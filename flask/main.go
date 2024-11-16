package main

import (
	"net/http"
	"github.com/gin-gonic/gin"
	"github.com/go-resty/resty/v2"
)

// Структуры для JSON данных
type CompatibilityRequest struct {
	UserCosmogram   map[string]interface{}   `json:"user_cosmogram"`
	GroupCosmograms []map[string]interface{} `json:"group_cosmograms"`
}

type CompatibilityResult struct {
	Results []map[string]interface{} `json:"results"`
}

// Адрес Python-алгоритма
const PythonServiceURL = "http://localhost:5002/algorithm"

func calculateCompatibility(c *gin.Context) {
	var req CompatibilityRequest

	// Чтение данных из запроса
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	// Запрос к Python-алгоритму
	client := resty.New()
	resp, err := client.R().
		SetHeader("Content-Type", "application/json").
		SetBody(req).
		Post(PythonServiceURL)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to reach Python service"})
		return
	}

	// Передача результата фронтенду
	c.Data(resp.StatusCode(), resp.Header().Get("Content-Type"), resp.Body())
}

func main() {
	router := gin.Default()

	// Роут для совместимости
	router.POST("/api/compatibility", calculateCompatibility)

	// Запуск API
	router.Run(":8080")
}
