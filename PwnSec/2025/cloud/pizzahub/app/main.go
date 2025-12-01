package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb/types"
	"github.com/aws/aws-sdk-go-v2/service/sqs"
	sqstypes "github.com/aws/aws-sdk-go-v2/service/sqs/types"

	"github.com/joho/godotenv"
)

type Order struct {
	Restaurant string   `json:"restaurant"`
	Customer   string   `json:"customer"`
	PizzaType  string   `json:"pizza_type"`
	PizzaSize  string   `json:"pizza_size"`
	Toppings   []string `json:"toppings,omitempty"`
	Notes      string   `json:"notes,omitempty"`
}

type Receipt struct {
	OrderID      string `json:"order_id"`
	Timestamp    string `json:"timestamp"`
	ClientName   string `json:"client_name"`
	DeliveryName string `json:"delivery_name"`
	Restaurant   string `json:"restaurant"`
	PizzaType    string `json:"pizza_type"`
	Size         string `json:"size"`
	Toppings     []string `json:"toppings"`
	Notes        string `json:"notes"`
}

var (
	sqsClient   *sqs.Client
	dynamoDB    *dynamodb.Client
	tableName   string
	sqsQueueURL string
)

func main() {
	if err := godotenv.Load(); err != nil {
		log.Println(".env file not found!")
	}

	ctx := context.Background()
	cfg, err := config.LoadDefaultConfig(ctx,
		config.WithRegion(getEnv("AWS_REGION", "eu-west-1")),
	)
	if err != nil {
		log.Fatalf("Unable to load AWS SDK config: %v", err)
	}

	sqsClient = sqs.NewFromConfig(cfg)
	dynamoDB = dynamodb.NewFromConfig(cfg)
	sqsQueueURL = getEnv("AWS_SQS_URL", "")
	tableName = getEnv("DYNAMODB_TABLE_NAME", "")

	fs := http.FileServer(http.Dir("./static/"))
	http.Handle("/", fs)
	http.HandleFunc("/order", orderHandler)
	http.HandleFunc("/receipt/", receiptHandler)

	port := getEnv("PORT", "8000")
	log.Printf("Server listening on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

func orderHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST allowed", http.StatusMethodNotAllowed)
		return
	}

	var order Order
	if err := json.NewDecoder(r.Body).Decode(&order); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	orderID := fmt.Sprintf("ORD-%d", time.Now().UnixNano())
	log.Printf("New order received: %s (%s %s %s)", orderID, order.Customer, order.PizzaType, order.PizzaSize)

	msgBody, err := json.Marshal(order)
	if err != nil {
		http.Error(w, "Internal error", http.StatusInternalServerError)
		return
	}

	sendInput := &sqs.SendMessageInput{
		QueueUrl:    &sqsQueueURL,
		MessageBody: aws.String(string(msgBody)),
		MessageAttributes: map[string]sqstypes.MessageAttributeValue{
			"OrderID": {
				DataType:    aws.String("String"),
				StringValue: aws.String(orderID),
			},
			"Restaurant": {
				DataType:    aws.String("String"),
				StringValue: aws.String(order.Restaurant),
			},
		},
	}

	resp, err := sqsClient.SendMessage(context.TODO(), sendInput)
	if err != nil {
		log.Printf("Failed to send message to SQS: %v", err)
		http.Error(w, "Failed to send order to SQS", http.StatusInternalServerError)
		return
	}

	log.Printf("Sent order %s to SQS --MessageId=%s", orderID, *resp.MessageId)

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"order_id": orderID,
		"status":   "Order placed successfully",
	})
}

func receiptHandler(w http.ResponseWriter, r *http.Request) {
	orderID := strings.TrimPrefix(r.URL.Path, "/receipt/")
	if orderID == "" {
		http.Error(w, "Missing order_id", http.StatusBadRequest)
		return
	}

	result, err := dynamoDB.GetItem(context.TODO(), &dynamodb.GetItemInput{
		TableName: aws.String(tableName),
		Key: map[string]types.AttributeValue{
			"order_id": &types.AttributeValueMemberS{Value: orderID},
		},
	})
	if err != nil {
		http.Error(w, "Failed to fetch receipt", http.StatusInternalServerError)
		return
	}

	if result.Item == nil {
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(map[string]string{"error": "Receipt not found"})
		return
	}

	var receipt Receipt
	if err := unmarshalDynamoDBItem(result.Item, &receipt); err != nil {
		http.Error(w, "Failed to parse receipt", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(receipt)
}

func unmarshalDynamoDBItem(item map[string]types.AttributeValue, out interface{}) error {
	m := make(map[string]interface{})
	for k, v := range item {
		m[k] = convertAttributeValue(v)
	}
	jsonBytes, _ := json.Marshal(m)
	return json.Unmarshal(jsonBytes, out)
}

func convertAttributeValue(av types.AttributeValue) interface{} {
	switch v := av.(type) {
	case *types.AttributeValueMemberS:
		return v.Value
	case *types.AttributeValueMemberN:
		return v.Value
	case *types.AttributeValueMemberB:
		return v.Value
	case *types.AttributeValueMemberSS:
		return v.Value
	case *types.AttributeValueMemberNS:
		return v.Value
	case *types.AttributeValueMemberBS:
		return v.Value
	case *types.AttributeValueMemberM:
		result := make(map[string]interface{})
		for key, value := range v.Value {
			result[key] = convertAttributeValue(value)
		}
		return result
	case *types.AttributeValueMemberL:
		result := make([]interface{}, len(v.Value))
		for i, value := range v.Value {
			result[i] = convertAttributeValue(value)
		}
		return result
	case *types.AttributeValueMemberNULL:
		return nil
	case *types.AttributeValueMemberBOOL:
		return v.Value
	default:
		return nil
	}
}

func getEnv(key, fallback string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return fallback
}
