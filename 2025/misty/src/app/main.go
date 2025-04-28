package main

import (
	"context"
	"flag"
	"log"
	"strings"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

func main() {
	// flags
	filePath := flag.String("filename", "", "Path to the file to upload")
	bucketName := flag.String("bucketname", "", "S3 bucket name")
	objectName := flag.String("objname", "", "Object name in the bucket")
	region := flag.String("region", "us-east-1", "S3 bucket region")
	endpoint := flag.String("endpoint", "localhost:9000", "S3 server endpoint")
	creds := flag.String("creds", "", "AccessKeyID:SecretAccessKey for S3 authentication")

	flag.Parse()

	if *filePath == "" || *bucketName == "" || *objectName == "" || *creds == "" {
		log.Fatalln("filename, bucketname, objname, and creds are required")
	}

	// parse creds
	parts := strings.SplitN(*creds, ":", 2)
	if len(parts) != 2 {
		log.Fatalln("Invalid creds format, expected AccessKeyID:SecretAccessKey")
	}
	accessKey := parts[0]
	secretKey := parts[1]

	ctx := context.Background()

	// createminio client
	minioClient, err := minio.New(*endpoint, &minio.Options{
		Creds:  credentials.NewStaticV4(accessKey, secretKey, ""),
		Secure: false, 
		Region: *region,
	})
	if err != nil {
		log.Fatalln("Error creating MinIO client:", err)
	}

	// upload file
	info, err := minioClient.FPutObject(ctx, *bucketName, *objectName, *filePath, minio.PutObjectOptions{})
	if err != nil {
		log.Fatalln("Error uploading file:", err)
	}

	log.Printf("Successfully uploaded %s of size %d bytes\n", *objectName, info.Size)
}
