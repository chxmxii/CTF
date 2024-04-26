package main

import (
    "bufio"
    "fmt"
    "os"
    "os/exec"
    "strings"
)

var (
    monkey     = `🙊`
    BLACKLIST  = []string{"|", "'", ";", "$", "\\", "#", "*", "&", "^", "@", "!", "<", ">", "%", ":", ",", "?", "{", "}", "`", "diff", "/dev/null", "patch", "./", "alias", "push", "strrev", "base64encode", "format", "file"}
    validChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;="
)

func isValidUTF8(text string) bool {
    for _, r := range text {
        if !strings.ContainsRune(validChars, r) {
            return false
        }
    }
    return true
}

func getTerraformCommands() []string {
    var commands []string
    scanner := bufio.NewScanner(os.Stdin)
    fmt.Println("Enter opentofu console commands (Enter an empty line to end):")
    for scanner.Scan() {
        user_input := scanner.Text()

        if user_input == "" {
            break
        }

        if !isValidUTF8(user_input) {
            fmt.Println(monkey)
            os.Exit(1337)
        }

        for _, command := range strings.Fields(user_input) {
            for _, blacklist := range BLACKLIST {
                if strings.Contains(command, blacklist) {
                    fmt.Println(monkey)
                    os.Exit(1337)
                }
            }
        }
        commands = append(commands, user_input)

        if len(commands) > 1 {
            fmt.Println(monkey)
            os.Exit(1337)
        }
    }
    return commands
}

func executeTerraformCommands(commands []string) {
    for _, command := range commands {
        cmd := exec.Command("tofu", "console")
        cmd.Stdin = strings.NewReader(command)
        output, err := cmd.CombinedOutput()
        if err != nil {
            fmt.Println("Error executing command:", err)
            os.Exit(1)
        }
        if strings.Contains(string(output), "0xL4ugh{Tf_sT4t3_AnDr0_T4t3}") {
            fmt.Println(monkey)
            os.Exit(1337)
        } else {
            fmt.Println(string(output))
        }
    }
}

func main() {
    commands := getTerraformCommands()
    executeTerraformCommands(commands)
}
