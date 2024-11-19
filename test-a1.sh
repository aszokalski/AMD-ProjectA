BASE_URL="http://localhost:3000"

echo "Training model for fungidata..."
    response=$(curl -s -X GET "$BASE_URL/train_model/fungidata")
    echo -e "\nModel training complete. Response:"
    echo "$response" | jq || echo "$response"
    echo "-------------------------------------"