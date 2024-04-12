## **Problem Statement Interpretation**

Our task is to develop a robust and scalable system that proactively identifies new generally available (GA) software products and checks their availability on the G2 software marketplace. The goal is to compile a list of products that are not yet listed on G2, simplifying the process of onboarding them onto the platform.

### **Key Objectives:**

1. **Identify New GA Products**: The system should periodically gather information about newly released software products.
2. **Check Availability on G2**: Utilize the G2 API to verify if identified products are listed on the platform.
3. **Compile a List**: Maintain a record of products that are not currently listed on G2.
4. **Streamline Onboarding**: Simplify the process of listing new products on G2.

## **Our Solution - [Discovery Dino](https://discovery-dino-rho.vercel.app/)** 

Welcome to Discovery Dino, your friendly assistant designed to simplify the process of discovering and listing the latest Generally Available (GA) software products on G2. We've developed a cloud-native solution deployed on AWS, ensuring scalability, robustness, and efficiency.

### **Solution Overview**

![Architecute Diagram](https://github.com/Sakthe-Balan/DiscoveryDino/tree/main/assets/DinoArch.png)

Our solution comprises three key sections, seamlessly integrated to streamline the product discovery and onboarding process.

### 1. Scraping and Data Acquisition

We've implemented a robust scraping mechanism to gather unstructured data from reliable sources. This data is streamed into Kafka and subsequently stored in our data lake on AWS S3, ensuring real-time ingestion and scalability. [More Information]

### 2. Data Processing and Ingestion

Once the data is stored in our data lake, our sophisticated data processing pipeline comes into play. Leveraging Large Language Models (LLMs) including OpenAI's GPT-3 and LLama2, hosted on our own instances, we process the data. This involves extracting features, categorizing products, identifying business types, and enhancing product descriptions. The processed data is then ingested into our MongoDB database, enabling seamless access and search functionalities. [More Information]

### 3. Data Analysis and Web Application

To empower users in navigating and interacting with the collected information, we've developed a user-friendly web application. This application acts as a co-pilot, offering intuitive features such as filtering, search capabilities, and AI-driven insights. Users can easily explore and identify new GA products, making informed decisions effortlessly. [More Information]

### **Key Features and Benefits**

- **Real-time Data Acquisition**: Continuous scraping and ingestion ensure up-to-date product information.
- **AI-powered Processing**: Utilizing LLMs for advanced data processing and enrichment.
- **Efficient Storage and Retrieval**: Data is stored in a scalable manner on AWS S3 and MongoDB.
- **Intuitive User Interface**: The web application provides a seamless experience for accessing and interacting with the data.
- **Scalable and Cloud-native**: Deployed on AWS, our solution can handle large volumes of data and user interactions without compromising performance.

## Installation

To set up and run Discovery Dino on your local machine, follow these steps:

1. Clone the repository:

   ```bash
   git clone <https://github.com/Sakthe-Balan/DiscoveryDino>

   ```

2. Download the environment file (`env`) from the provided link and place it in the project directory.

   - `.env.template`

     ```json
     MONGO_URI=
     DB_NAME=

     AWS_ACCESS_KEY_ID=
     AWS_SECRET_ACCESS_KEY=
     AWS_REGION=

     OPENAI_API_KEY=
     SERPAPI_API_KEY=
     G2_API_KEY=
     LEPTON_API_KEY=
     ```

3. **Backend Setup**:

   ```bash
   cd DiscoveryDino/server
   pip install -r requirements.txt
   python main.py

   ```

4. **Frontend Setup**:

   ```bash
   cd DiscoveryDino/discoverydino
   npm install
   npm run build
   npm start

   ```
**WARNING:** If you want to scrape locally, make sure your Kafka server is set up and the URL is given accordingly(check out the kafka folder). Instead, use `s3_spiders` which directly puts to S3.

### Using Docker

Alternatively, you can use Docker to run Discovery Dino:

1. Build and Run the Frontend and Backend Images:

   ```bash
   docker-compose up

   ```



By following these steps, you'll have Discovery Dino up and running locally, ready to explore and discover the latest Generally Available (GA) software products effortlessly.

## Tech Stack and Why

Our technology stack for Discovery Dino is carefully selected to ensure scalability, performance, and ease of development. Each component plays a crucial role in delivering a robust and efficient solution.

### Backend

- **FastAPI**: FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3. It's asynchronous and efficient, making it ideal for our backend API services.
- **MongoDB**: MongoDB is a NoSQL database that provides flexibility and scalability for handling unstructured data. It's well-suited for our use case of storing and retrieving product information efficiently.
- **Kafka**: Kafka is used for stream processing and real-time data ingestion. It enables scalable and reliable messaging between different components of our system.
- **QdrantDB**: QdrantDB is a high-performance vector database optimized for similarity search and recommendation systems. It enhances our data analysis capabilities for efficient product categorization and search.

### Frontend

- **Next.js**: Next.js is a React framework for building server-rendered applications. It offers benefits like improved SEO, faster page loading, and efficient routing, making it ideal for our web application.

### Cloud Infrastructure

- **AWS (Amazon Web Services)**:
  - **Lambda**: AWS Lambda allows us to run serverless functions, enabling event-driven architectures and reducing operational overhead.
  - **EC2 (Elastic Compute Cloud)**: EC2 provides scalable compute capacity in the cloud, allowing us to host and run our backend services.
  - **S3 (Simple Storage Service)**: AWS S3 is used as our data lake for storing scraped data and other assets securely and at scale.

### Why This Stack?

- **Performance**: FastAPI, Kafka, and QdrantDB are chosen for their high performance, enabling real-time data processing and efficient querying.
- **Scalability**: AWS services (Lambda, EC2, S3) provide scalability and flexibility, allowing us to handle varying workloads and data volumes effectively.
- **Ease of Development**: Next.js simplifies frontend development with its built-in features like automatic code splitting, server-side rendering, and routing.

## Scraping and Data Acquisition Details

Our scraping and data acquisition process is designed to efficiently gather product information from various sources and store it in a structured manner for further processing.

### Setup and Architecture

1. **Kafka Server Setup**:
   - Start by setting up the Kafka server as described in the instructions provided in the `kafka` folder. The `consumer.py` script handles the consumption of data streamed by crawlers to the producer, which then uploads it into the designated S3 bucket.
2. **Crawlers**:
   - Inside the `dino` folder, we have two sets of crawlers:
     - **s3_spiders**: These crawlers directly push JSON data to the S3 bucket without using Kafka.
     - **spiders**: These crawlers utilize Kafka architecture to stream each scraped JSON to Kafka before uploading to S3.
3. **Concurrent Spider Execution**:
   - The spiders are designed to run concurrently, with each spider executing as a separate background process. This parallel execution enables efficient scraping of data from multiple sources simultaneously.
4. **FastAPI Server Integration**:
   - All functionalities related to running the spiders, querying databases, and preprocessing scraped data are defined within the `main.py` of our FastAPI server.
   - The FastAPI server provides endpoints to start, stop, and monitor the status of individual spiders, as well as a mechanism to trigger concurrent scraping of all spiders.
5. **Template for Creating Scrapers**:
   - We provide a `spider_template.py` that simplifies the process of creating new scrapers for additional websites. This template includes placeholders for inserting scraping selectors and generating JSON output.
6. **Environment Setup**:
   - Each crawler requires its own environment variables defined in an `.env` file (template provided). Ensure proper setup of these variables before running the crawlers.

### Replicating the Setup Locally

To recreate the scraping and data acquisition process locally, follow these steps:

1. Install required dependencies:

   ```bash
   pip install -r requirements.txt

   ```

2. Setup Kafka server and `consumer.py` (instructions in the `kafka` folder). Alternatively, use `s3_spiders` if you prefer direct data upload to S3.
3. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload

   ```

4. Trigger the scraping process:
   - Invoke the `/scrape` endpoint of the FastAPI server (`http://localhost:8000/scrape`) to start the scraping process.

By following these steps, you can replicate our scraping and data acquisition pipeline locally and explore the functionalities of Discovery Dino's backend system.

---

## Data Processing and Ingestion

After acquiring semi-structured data stored in S3, the data processing and ingestion phase involves transforming and enriching the data for meaningful analysis and storage.

### Workflow Overview

1. **Dynamic Data Retrieval**:
   - Retrieve the latest files from the designated S3 bucket dynamically, downloading them onto serverless containers for temporary processing.
2. **Data Batch Processing**:
   - Batch process the downloaded data, focusing on understanding product details and identifying existing entries on G2 to minimize API calls.
3. **Utilizing Language Models (LLMs)**:
   - For detailed product descriptions, leverage LLMs such as GPT-3 and LLama2 (hosted on our own cluster) to enhance and enrich product information.
4. **Feature Extraction and Categorization**:
   - Extract features like categories and identify business types (B2B or B2C) to enhance product understanding and categorization.
5. **Integration with External APIs**:
   - Integrate with external APIs (e.g., Google Search API) to supplement data and gather the latest information where feasible.
6. **Database Integration**:
   - Push processed and enriched data into MongoDB, ensuring a structured and organized repository of product information.

### MongoDB Design

- MongoDB is structured to store detailed product entries, including descriptions, categories, business types, and metadata.
- The database is continuously updated with new product information sourced from the scraping and ingestion pipeline.

By following this data processing and ingestion workflow, Discovery Dino ensures that product information is systematically analyzed, enriched, and stored for efficient retrieval and analysis.

---

## Data Analysis and Web Application

Our web application provides a user-friendly interface to explore and interact with the collected product data, offering intuitive features for enhanced discovery and decision-making.

### Key Features of the Web Application

1. **Dynamic Dashboard**:
   - Display all scraped products that are not yet listed on G2, providing visibility into potential additions to the platform.
2. **Filtering and Sorting**:
   - Implement filters based on star ratings, categories, and other criteria to refine product searches.
3. **Dynamic Search**:
   - Enable users to search the entire database for specific products or keywords, ensuring quick access to relevant information.
4. **Detailed Product Information**:
   - View detailed product descriptions, website links, ratings, and reviews with a single click for comprehensive insights.
5. **Integration with Database**:
   - Query product data directly from the MongoDB database, which is continuously updated with fresh information from the preprocessing pipeline.

Our web application acts as a powerful tool for software discovery, leveraging the processed data to facilitate informed decision-making and effortless navigation of the vast landscape of B2B software products. Experience the convenience of Discovery Dino's user-centric interface for exploring the latest Generally Available (GA) products!

### Database Design

In our Discovery Dino project, we have designed a MongoDB database to efficiently store and manage various types of product information, categorizing them based on their source, filtering status, and existing presence on the G2 platform.

### Collections

1.  **`scraped_products`**:
    This collection contains all products that have been scraped, providing detailed information for search and analysis purposes.

    ````json
    {
    "\_id": "string",
    "productName": "string",
    "photoUrl": "string",
    "description": "string",
    "rating": 0,
    "similarProducts": ["list of URLs"],
    "contactMail": "string",
    "website": "string",
    "category": ["string"],
    "additionalInfo": "string",
    "scarpedLink": "string",
    "reviews": [{"objects"}]
    }

        ```

    ````

2.  **`filtered_products`**:
    This collection stores products that have been filtered as B2B and are not currently listed on G2.

    ````json
    {
    "\_id": "string",
    "productName": "string",
    "photoUrl": "string",
    "description": "string",
    "rating": 0,
    "similarProducts": ["list of URLs"],
    "contactMail": "string",
    "website": "string",
    "category": ["string"],
    "additionalInfo": "string",
    "scarpedLink": "string",
    "reviews": [{"objects"}]
    }

        ```

    ````

3.  **`g2_products`**:
    This collection serves as a cache for products already listed on G2, storing relevant metadata and associations.

    ````json
    {
    "associatedProductName": "product name for which we got this result",
    "id": "129d01fa-f6db-4477-a3f2-549cee2b6d54",
    "type": "products",
    "links": {},
    "attributes": {},
    "relationships": {}
    }

        ```
    ````

### Categories

We have predefined categories to classify products based on their nature and functionality, enabling efficient organization and filtering.

```bash
categories = [
  "Sales Tools",
  "Marketing",
  "Analytics Tools & Software",
  "Artificial Intelligence",
  "AR/VR",
  "B2B Marketplaces",
  "Business Services",
  "CAD & PLM",
  "Collaboration & Productivity",
  "Commerce",
  "Content Management",
  "Converged Infrastructure",
  "Customer Service",
  "Data Privacy",
  "Design",
  "Development",
  "Digital Advertising Tech",
  "Ecosystem Service Providers",
  "ERP",
  "Governance, Risk & Compliance",
  "Greentech",
  "Hosting",
  "HR",
  "IoT Management",
  "IT Infrastructure",
  "IT Management",
  "Marketing Services",
  "Marketplace Apps",
  "Office",
  "Other Services",
  "Professional Services",
  "Routers",
  "Security"
]

```

### S3 Design

Our data lake setup in Amazon S3 organizes scraped data into a structured format for further processing and analysis.

### Sample Data Structure

```json
{
  "title": "Workspace ONE",
  "description": "Workspace ONE is a user-friendly intelligence-driven digital workspace solution that enables users to securely manage and deliver any app anywhere and on any device. It provides one source of truth for end user access, provisioning, security, compliance, and management across all devices",
  "price": "4.7",
  "image_url": "data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27104%27%20height=%27104%27/%3e",
  "link": "<https://www.softwareadvice.com/help-desk/workspace-one-profile/>",
  "additional_info": "Workspace ONE is a user-friendly intelligence-driven digital workspace solution that enables users to securely manage and deliver any app anywhere and on any device. It provides one source of truth for end user access, provisioning, security, compliance, and management across all devices",
  "website": "<https://www.vmware.com/products/workspace-one.html>",
  "reviews": [
    { "content": "Remote user access, application/desktop virtualization." },
    {
      "content": "The implementation took some time but all of our end-users are extremely happy to be off the legacy MDM platform."
    },
    {
      "content": "IT implemented it and I was tasked with enforcing security controls and policies. Integrating it with our SIEM has been a huge pain so we ended up going with something else. Forcing HD encryption to all endpoints was nice."
    }
  ]
}
```

### Mapping to Database Schema

- `title` → `productName`
- `description` → `description`
- `price` → `rating`
- `image_url` → `photoUrl`
- `link` → `scarpedLink`
- `additional_info` → `additionalInfo`
- `website` → `website`
- `reviews` → `reviews`

### Data Processing and Ingestion

The data processing phase involves dynamically retrieving data from S3, processing it for detailed insights, and storing the enriched data in MongoDB for further analysis and application usage. This workflow ensures that product information is organized, categorized, and made accessible for effective decision-making.

---

By implementing this comprehensive database design and data processing workflow, Discovery Dino optimizes the handling and utilization of scraped product data, enabling efficient discovery and analysis of B2B software products.

# API Documentation

This document provides detailed information on the API endpoints of the FastAPI application.

## General Information

Each endpoint in this documentation includes details about its purpose, the parameters it requires, and the expected response format.

---

### 1. Base Function

**Endpoint:** `/`

**Method:** `GET`

**Parameters:** None

**Response:**
- **Type:** JSON
- **Content:**
  - `message`: Welcome message and service information.
  - `DB_Status`: Status of the MongoDB connection.

**Description:**
Provides basic information about the service, including the status of the connection to MongoDB.

---

### 2. Get Data

**Endpoint:** `/api/data`

**Method:** `GET`

**Parameters:**
- **limit** (int): The number of documents to retrieve.

**Response:**
- **Type:** JSON
- **Content:** An array of documents from the specified MongoDB collection.

**Description:**
Retrieves a specified number of documents from a MongoDB collection.

---

### 3. Search Data

**Endpoint:** `/api/search`

**Method:** `GET`

**Parameters:**
- **collection** (str): Name of the MongoDB collection to search in.
- **searchString** (str, optional): String to search for within the productName field.
- **limit** (int, optional): The number of documents to retrieve.

**Response:**
- **Type:** JSON
- **Content:**
  - `collection`: The MongoDB collection searched.
  - `searchString`: The string searched for.
  - `results`: An array of search results.

**Description:**
Searches for a specific string within a specified collection based on the productName field.

---

### 4. Filter Data

**Endpoint:** `/api/filter`

**Method:** `GET`

**Parameters:**
- **collection** (str): Name of the MongoDB collection to search in.
- **rating** (str, optional): The number of stars to filter from.
- **category** (str, optional): Category to filter from.
- **limit** (int, optional): The number of documents to retrieve.

**Response:**
- **Type:** JSON
- **Content:**
  - `collection`: The MongoDB collection searched.
  - `results`: An array of documents that meet the filter criteria.

**Description:**
Applies filters to the data based on rating and category within a specified collection.

---

### 5. Scrape Data

**Endpoint:** `/scrape`

**Method:** `GET`

**Parameters:** None

**Response:**
- **Type:** JSON
- **Content:**
  - `message`: Message indicating scraping completion.

**Description:**
Initiates scraping by starting spiders in separate processes.

---

### 6. Stop Spider

**Endpoint:** `/stop_spider/{spider_name}`

**Method:** `POST`

**Parameters:**
- **spider_name** (str): The name of the class of the spider to stop.

**Response:**
- **Type:** JSON
- **Content:**
  - `message`: Message indicating whether the spider was stopped successfully.

**Description:**
Stops a running spider by its class name.

---

### 7. Run Specific Spider

**Endpoint:** `/run_spider/{spider_name}`

**Method:** `GET`

**Parameters:**
- **spider_name** (str): The name of the class of the spider to be run.

**Response:**
- **Type:** JSON
- **Content:**
  - `message`: Message indicating whether the spider was started successfully.

**Description:**
Runs a specific spider by name, initiating a new process.

---


## Contribution

We welcome contributions to Discovery Dino from the community. If you are interested in contributing to the project, please check out our GitHub repositories:

- [Sakthe Balan's GitHub](https://github.com/Sakthe-Balan)
- [Adithya S K's GitHub](https://github.com/adithya-s-k)

Feel free to submit pull requests or open issues to collaborate and improve the project.

## Contact

For any project-related inquiries or issues, please contact:

- Email: [sakthebalan2003@gmail.com](mailto:adithyaskolavi@gmail.com)
- Email: [adithyaskolavi@gmail.com](mailto:adithyaskolavi@gmail.com)

Our team is available to address any questions, feedback, or concerns you may have regarding Discovery Dino.

## Conclusion

Discovery Dino is a powerful tool designed to simplify the process of discovering and onboarding new Generally Available (GA) software products onto the G2 platform. With robust data scraping, processing, and a user-friendly web interface, Discovery Dino empowers users to explore and interact with a comprehensive database of B2B software products.

By leveraging advanced technologies and a scalable architecture, Discovery Dino aims to contribute to informed decision-making in software purchasing and promote the visibility of emerging software solutions.

Explore the world of B2B software discovery with Discovery Dino today!
