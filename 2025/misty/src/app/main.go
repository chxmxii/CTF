package main

import (
	"context"
	"log"
	"flag"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

var (
	Cfg = struct {
		EndPoint        string
		AccessKeyID     string
		SecretAccessKey string
		UseSSL          bool
	}{
		EndPoint:        "localhost:9000",
		AccessKeyID:     "HY2vJl0vhYEUuJt0hpq3",
		SecretAccessKey: "xdifadKQpR06W7do2w6oZsJD40hnUK9KmPY6Oq7V",
		UseSSL:          false,
	}

	BucketName = "test-mist37"
	Location   = "us-west-1"
)

func main() {
	ctx := context.Background()

	// init minio client
	minioClient, err := minio.New(Cfg.EndPoint, &minio.Options{
		Creds:  credentials.NewStaticV4(Cfg.AccessKeyID, Cfg.SecretAccessKey, ""),
		Secure: Cfg.UseSSL,
	})
	if err != nil {
		log.Fatalln("Failed to initialize MinIO client:", err)
	}

	// create bucket
	err = minioClient.MakeBucket(ctx, BucketName, minio.MakeBucketOptions{Region: Location})
	if err != nil {
		exists, errBucketExists := minioClient.BucketExists(ctx, BucketName)
		if errBucketExists == nil && exists {
			log.Printf("We already own bucket %s\n", BucketName)
		} else {
			log.Fatalln("Failed to create bucket:", err)
		}
	} else {
		log.Printf("Successfully created bucket %s\n", BucketName)
	}

	// upload file
	filePath := flag.String("file", "", "file to be uploaded")
	objectName := flag.String("obj-name", "", "object name")
	contentType := flag.String("content-type","application/octet-stream", "content type")

	flag.Parse()

	info, err := minioClient.FPutObject(ctx, BucketName, *objectName, *filePath, minio.PutObjectOptions{ContentType: *contentType})
	if err != nil {
		log.Fatalln("Failed to upload file:", err)
	}

	log.Printf("Successfully uploaded %s of size %d bytes\n", objectName, info.Size)
}
