#!/bin/bash

BASE_URL="http://localhost:3000"
INPUT_FILE="input.json"

train_model() {
    echo "Training model..."
    response=$(curl -s -X GET "$BASE_URL/train_model/medknow")
    echo -e "\nModel training complete. Response:"
    echo "$response" | jq || echo "$response"
    echo "-------------------------------------"
}

predict_OneR() {
    if [[ -f "$INPUT_FILE" ]]; then
        echo "Predicting with OneR model using input from $INPUT_FILE..."
        response=$(curl -s -X POST "$BASE_URL/predict/medknow/OneR" \
            -H "Accept: application/json" \
            -H "Content-Type: application/json" \
            -d @"$INPUT_FILE")
        echo -e "\nOneR prediction complete. Response:"
        echo "$response" | jq || echo "$response"
        echo "-------------------------------------"
    else
        echo "Input file $INPUT_FILE not found!"
        exit 1
    fi
}

predict_ID3() {
    if [[ -f "$INPUT_FILE" ]]; then
        echo "Predicting with ID3 model using input from $INPUT_FILE..."
        response=$(curl -s -X POST "$BASE_URL/predict/medknow/ID3" \
            -H "Accept: application/json" \
            -H "Content-Type: application/json" \
            -d @"$INPUT_FILE")
        echo -e "\nID3 prediction complete. Response:"
        echo "$response" | jq || echo "$response"
        echo "-------------------------------------"
    else
        echo "Input file $INPUT_FILE not found!"
        exit 1
    fi
}

# Run each function in sequence
train_model
predict_OneR
predict_ID3