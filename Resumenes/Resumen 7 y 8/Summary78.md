# Summary 7 and 8

> Gabriela Gutiérrez Valverde - 2019024089

## Book 1
> neo4j: 5 Use Cases for Graph Tecnology

Neo4j helps by identifying connections and plotting relationships otherwise unseen.

1. **Fraud Detection:** powers a proprietary fraud detection application capable of sustaining hundreds of transactions a second, spending merely tens of milliseconds on a single query.
2. **Real-Time Recommendations:** recommendation system generates a detailed model of all the actions customers take on the website, helping to optimize the system. 
3. **Bill of Materials:** rapidly collects and combines massive amounts of information and saves analysts huge amounts of time. Answers are immediate.
4. **Track & Trace:** enables people to find out the status of a product wherever it is in the supply chain and to identify and verify its path.
5. **Network & IT Ops:** The graph’s connected structure enables network managers to conduct sophisticated impact analyses, such as, discovering  which parts of the network particular customers depend on.

## Book 2
> neo4j: The return on Connected Data

### Connections Unlock the Value of Data
Increasing data’s connectedness further increases its value through additional context. The value isn’t in disparate data but in the relationships, or connections, between the data.

- **Traditional Database:** finding connections takes another tool and considerable processing work. And connections are not stored.
- **neo4j:** stores connections with the data, no extra work.

Without connected data, organizations lack key information that’s necessary to obtain a 360-degree view of a customer, build a complete network topology, deliver relevant recommendations in real-time, or obtain the visibility required to prevent fraud. 

**Benefits of Connected Data**
-  the ability to provide a connected view of the data to your analytic and operational applications, thereby gaining and growing intelligence downstream.
-  obtain context that allows you to more deeply or better refine the pieces of information you’re collecting or the recommendations you’re producing.
-  better understand the flow of money to detect fraud and money laundering, and assess the risk of a network outage across computer networks.
-  helps you see when and how relationships change over time.

Connected data is most powerful when it provides operational, real-time insights and not just after-the-fact analytics. Real-time insights allow business users and applications to make business decisions and act in real-time.

**Graph Database**
- makes it easy to express and persist relationships across many types of data elements.
- highly scalable transactional and analytic database that stores data relationships as first-class entities.
- each node represents an entity, and each relationship represents how two nodes are associated.
- simple and agile due to their schema-optional nature.
- can be easily changed or updated
- can automatically determine the data typing, and additional nodes can be added at any time.

## Book 3
> neo4j: A Brief Introduction to Graph Data Platforms

### What Are Graph Databases Good for?

- **Fraud Detection & Analytics:** Real-time analysis of data relationships is essential to uncovering fraud rings.
- **Artificial Intelligence & Machine Learning:** AI winners and losers will be decided based on who harnesses context within data for a true competitive advantage. 
- **Real-Time Recommendation Engines:**  Graph-powered recommendation engines help companies personalize products, content and services.
- **Knowledge Graphs:**  are the basis for many natural language processing (NLP) and AI solutions.
- **Network & Database Infrastructure Monitoring:** more suitable than RDBMS for making sense of complex interdependencies central to managing networks, data centers, cybersecurity and IT infrastructure. 
- **Master Data Management (MDM):** allows you to organize and manage your master data with flexibility.

Graph databases tackle the most harrowing of data problems, like:

- Vastly different views of the data model between business and technology teams
- Lack of schema flexibility and adaptability
- The “JOIN problem” 

**Traditional Technology Choices Do Not Consider How Data Is Interrelated**
Relational databases are not well-suited for modeling and storing today’s highly connected and agile datasets. Traditional RDBMS technology has a difficult time expressing and revealing how real and virtual entities are related. Columns and rows aren’t how data exists in the real world.

### Collections vs. Connections

**SQL & NoSQL Systems Focus on Data Aggregation & Collection**
Collection-centric storage designs as implemented by SQL and Not only SQL (NoSQL) databases are designed to efficiently divide and store data. These systems were born during the era of scarce physical memory and expensive disk-based storage, designed to avoid managing often-redundant data objects because disk space was costly. NoSQL systems like document, wide column and key-value data stores carry those concepts forward (and backward) by simplifying their models in exchange for higher levels of scale and simplicity. None of these systems focus on interrelated, contextualized data or how that data might be traversed to reveal unobvious relationships.

**Graph Systems Focus on Data Connections**
Graph database technologies focus on how data elements are interrelated and contextualized as connected data. _Connected data_ is the materialization and harnessing of relationships between data elements, which is modeled as a property graph. In the graph model, data relationships are persisted so they can be navigated or traversed along connected paths to gain context. Relationships are both typed and directional. 

### Benefits of Graph Databases

- **Simple and natural data modeling:** provide flexibility for data modeling, depending on relationship types.
- **Flexibility for evolving data structures:** provides flexible schema evolution.
- **Simultaneous support for real-time updates and queries:** allow real-time updates on graph data while supporting queries concurrently.
- **Better, faster and more powerful querying and analytics:** provide superior query performance with connected data using native storage and native indexed data structure.





































