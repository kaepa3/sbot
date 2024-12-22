package main

import (
	"context"
	"fmt"
	"github.com/joho/godotenv"
	"github.com/nasa9084/go-switchbot"
	"os"
)

var (
	openToken string
	secretKey string
)

func main() {
	loadEnv()
	c := switchbot.New(openToken, secretKey)
	pdev, inDev, _ := c.Device().List(context.Background())

	for _, d := range inDev {
		fmt.Printf("%s\t%s\n", d.Type, d.Name)
		if d.Name == "ライト" {
			cmd := switchbot.DeviceCommandRequest{
				Command:     "turnOn",
				Parameter:   "default",
				CommandType: "command",
			}
			err := c.Device().Command(context.Background(), d.ID, cmd)
			if err != nil {
				fmt.Println(err)
			}
		}
	}
	for _, d := range pdev {
		fmt.Printf("%s\t%s\n", d.Type, d.Name)
		st, err := c.Device().Status(context.Background(), d.ID)
		if err != nil {
			fmt.Println(err)
		} else {
			fmt.Println(st)
		}
	}
}
func loadEnv() error {
	err := godotenv.Load(".env")
	if err != nil {
		return err
	}
	openToken = os.Getenv("OPENTOKEN")
	secretKey = os.Getenv("SECRETKEY")
	return nil
}
