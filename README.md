# Data Mining Chatbot

Welcome to the source code repository for my **Data Mining Chatbot**! You can try the chatbot live here:

[**Data Mining Chatbot Frontend**](http://my.chat.frontend.nicka.s3-website.us-east-2.amazonaws.com/)

## Overview
This chatbot leverages state-of-the-art natural language processing techniques to answer questions about **Data Mining**. It is built using:

- **LlamaIndex**: Used to split content from three popular Data Mining textbooks and create a `VectorStoreIndex` for efficient query processing.
- **LangChain**: Integrated with the `gpt-3.5-turbo` language model to process and respond to user queries.
- **AWS Cloud Services**:
  - **Lambda**: Hosted the main chatbot logic as a serverless function using a Docker image container.
  - **S3 Buckets**: Used for storing the `VectorStoreIndex` and hosting the frontend web page.
  - **API Gateway**: Connected the frontend to the Lambda function, enabling real-time interaction.

## Features
- **Data Mining Expertise**: Trained on the content of three renowned Data Mining textbooks.
- **State-of-the-Art NLP**: Powered by GPT-3.5 Turbo, ensuring accurate and contextual responses.
- **Cloud Deployment**: Fully deployed on AWS for public accessibility.

## Project Structure
- **Backend**: Python-based implementation of the chatbot logic, hosted in AWS Lambda.
- **Frontend**: A simple web interface stored in an S3 bucket for users to interact with the chatbot.
- **Infrastructure**: API Gateway acts as the middleware between the frontend and the backend.

## How It Works
1. **Index Creation**: Textbooks were processed using LlamaIndex to create a searchable VectorStore.
2. **Query Handling**: LangChain and GPT-3.5 Turbo handle queries by leveraging the VectorStore to provide precise answers.
3. **Deployment**: The backend logic runs in a serverless AWS Lambda function, while the frontend is hosted on an S3 bucket with a public-facing URL.

## Usage
Feel free to explore the code and adapt it for your own projects. Whether you’re building an educational chatbot or experimenting with cloud-based AI services, this repository provides a solid foundation.

## Deployment
The project is designed to be deployed on AWS. To replicate the deployment:
- Build the Docker image for the Lambda function.
- Configure API Gateway and S3 buckets.
- Upload the VectorStoreIndex and frontend files to the appropriate S3 buckets.
- Link the Lambda function to the API Gateway and test the setup.

## Contributions
Contributions are welcome! If you have suggestions, improvements, or new features in mind, feel free to open an issue or submit a pull request.

## License
This project is open-source and available under the [MIT License](LICENSE). You are welcome to use, modify, and build upon this project.

---
**Enjoy exploring Data Mining with this chatbot!**
