# Formative

Microservices Modeling

## Question

What are some foundational concepts that influence the design and boundaries of microservices?

- Information hiding
- Coupling
- Cohesion
- [ ] Ubiquitous language

### Rationale

- Correct. Information hiding is a key concept in microservices design.
- Correct. Coupling is a fundamental concept that influences the boundaries of microservices.
- Correct. Cohesion is another important concept in microservices design.
- Incorrect. Ubiquitous language is a core concept of domain-driven design, not a foundational
  concept for microservices design.

## Question

What is a useful technique for modeling microservices?

- [ ] Volatility-based decomposition
- [ ] Technology-based decomposition
- Domain-driven design
- [ ] All of the above

### Rationale

- Incorrect. While volatility-based decomposition can be used to establish microservice boundaries,
  it is not specifically mentioned as a technique for modeling microservices in the text.
- Incorrect. Similarly, technology-based decomposition can be used to establish microservice
  boundaries, but it is not specifically mentioned as a technique for modeling microservices in the
  text.
- Correct. The text specifically mentions domain-driven design as a hugely useful technique for
  modeling microservices.
- Incorrect. While all of these techniques can be used in the context of microservices, only
  domain-driven design is specifically mentioned as a technique for modeling microservices in the text.

## Question

What is the purpose of thinking about the boundaries of your microservices?

- To maximize the benefits of microservices
- To avoid potential downsides of microservices
- [ ] To ensure that all microservices are of equal size
- [ ] To make sure that all microservices use the same technology stack

### Rationale

- Correct. The text mentions that thinking about the boundaries of your microservices can help
  maximize their benefits.
- Correct. The text also mentions that considering the boundaries of your microservices can help
  avoid potential downsides.
- Incorrect. The size of microservices is not mentioned in the text as a reason for thinking about
  their boundaries.
- Incorrect. The technology stack used by microservices is not mentioned in the text as a reason for
  thinking about their boundaries.

# Formative

Microservices in MusicCorp

## Question

What is the primary reason MusicCorp is considering the use of microservices?

- [ ] To compete with Spotify
- [ ] To improve their website
- To make changes as easily as possible
- [ ] To revive the vinyl record business

### Rationale

- While MusicCorp is aware of Spotify, the text does not indicate that they are directly trying to
  compete with them through the use of microservices.
- Improving their website might be a benefit of using microservices, but the text does not state this
  as the primary reason.
- Correct. The text states that MusicCorp believes its best chance of success is to be able to make
  changes as easily as possible, which is a key benefit of microservices.
- The text mentions the decline of the vinyl record business, but does not suggest that microservices
  will be used to revive it.

## Question

What is the current state of MusicCorp's understanding and application of modern technology trends?

- They are a little behind the curve
- [ ] They are leading the industry
- [ ] They are on par with industry standards
- [ ] They are slightly ahead of the curve

### Rationale

- Correct. The text states that MusicCorp is "a little behind the curve", indicating that they are
  not fully up-to-date with modern technology trends.
- The text does not suggest that MusicCorp is leading the industry in terms of technology trends.
- The text suggests that MusicCorp is not on par with industry standards, as they are described as
  being "a little behind the curve".
- The text does not suggest that MusicCorp is slightly ahead of the curve in terms of technology
  trends.

# Summative

Microservices and Domain-Driven Design

## Question

Based on the text, which foundational concept of microservices is MusicCorp primarily interested in?

- [ ] Information hiding
- [ ] Coupling and cohesion
- Ability to make changes easily
- [ ] Domain-driven design

### Rationale

- While information hiding is a foundational concept of microservices, the text does not specifically
  mention this as a focus for MusicCorp.
- Coupling and cohesion are important concepts in microservices, but the text does not specifically
  mention these as a focus for MusicCorp.
- Correct. The text states that MusicCorp's main interest in microservices is the ability to make
  changes

# Formative

Microservices Boundary Design

## Question

What is the most important underlying idea to keep in mind when creating microservices?

- [ ] Microservices should be created as quickly as possible.
- Microservices should be able to be changed and deployed independently.
- [ ] Microservices should always interact with each other over the network.
- [ ] Microservices should always be created in large teams.

### Rationale

- Speed of creation is not the most important factor in microservices design.
- Correct. The ability to change and deploy microservices independently is vital.
- While network-based interaction is a characteristic of microservices, it is not the most important
  underlying idea.
- The size of the team creating the microservices is not the most important factor.

## Question

Which three key concepts are vital to grasp when working out what makes for a good microservice
boundary?

- Information hiding
- Cohesion
- Coupling
- [ ] Network-based interaction

### Rationale

- Correct. Information hiding is a key concept in defining microservice boundaries.
- Correct. Cohesion is a key concept in defining microservice boundaries.
- Correct. Coupling is a key concept in defining microservice boundaries.
- While network-based interaction is a characteristic of microservices, it is not one of the three
  key concepts for defining microservice boundaries.

## Question

Microservices are just another form of what?

- [ ] Network-based interaction
- [ ] Large team collaboration
- Modular decomposition
- [ ] Rapid development

### Rationale

- Network-based interaction is a characteristic of microservices, but it is not what microservices
  are a form of.
- The size of the team working on microservices does not define what microservices are a form of.
- Correct. Microservices are a form of modular decomposition.
- The speed of development does not define what microservices are a form of.

# Formative

Microservices and Information Hiding

## Question

Who developed the concept of information hiding and why is it important in defining module boundaries
in microservices?

- David Parnas
- [ ] Adrian Colyer
- [ ] James Evans, Sr.
- [ ] John Amos

### Rationale

- Correct. David Parnas developed the concept of information hiding to effectively define module
  boundaries. This concept is crucial in microservices as it allows for independent development,
  comprehensibility, and flexibility of modules.
- Adrian Colyer examined David Parnas's papers with respect to microservices, but he did not develop
  the concept of information hiding.
- James Evans, Sr. and John Amos are unrelated to this topic.

## Question

What are the three desirable characteristics that Parnas describes which are amplified by the use of
microservices?

- Improved development time
- Comprehensibility
- Flexibility
- [ ] Scalability

### Rationale

- Correct. By allowing modules to be developed independently, more work can be done in parallel,
  reducing the impact of adding more developers to a project.
- Correct. Each module can be looked at and understood in isolation, making it easier to understand
  what the system as a whole does.
- Correct. Modules can be changed independently from one another, allowing for changes to be made to
  the functionality of the system without requiring other modules to change.
- Scalability is a benefit of microservices, but it is not one of the three characteristics that
  Parnas describes.

## Question

How does reducing the number of assumptions that one module (or microservice) makes about another
impact the connections between them?

- It makes it easier to change one module without impacting others
- [ ] It increases the complexity of the connections between modules
- [ ] It requires more developers to manage the connections between modules
- [ ] It reduces the comprehensibility of the system

### Rationale

- Correct. By keeping the number of assumptions small, it is easier to ensure that we can change one
  module without impacting others.
- Reducing the number of assumptions simplifies the connections between modules, not increases their
  complexity.
- The number of developers needed to manage the connections between modules is not directly related
  to the number of assumptions made by the modules.
- Reducing the number of assumptions actually improves the comprehensibility

# Formative

Microservices and Cohesion

## Question

What is a succinct definition of cohesion in the context of microservices?

- [ ] The code that is written together, stays together.
- The code that changes together, stays together.
- [ ] The code that is deployed together, stays together.

### Rationale

- This option is incorrect because cohesion is not about when the code is written, but how it
  changes.
- Correct. This definition emphasizes that related behavior should be grouped together for ease of
  making changes.
- This option is incorrect because cohesion is not about when the code is deployed, but how it
  changes.

## Question

Why is it important to have related behavior sit together in microservices?

- It allows changes to be made in one place and released as soon as possible.
- [ ] It allows changes to be made in many places and released at the same time.
- [ ] It allows changes to be made in one place and released at the same time.

### Rationale

- Correct. Grouping related behavior together allows changes to be made in one place and released as
  soon as possible, which is faster and less risky.
- This option is incorrect because making changes in many places and releasing them at the same time
  is slower and riskier.
- This option is incorrect because it combines elements of the correct and incorrect options.

## Question

What does it mean if related functionality is spread across the system in the context of
microservices?

- [ ] The system has strong cohesion.
- The system has weak cohesion.
- [ ] The system has no cohesion.

### Rationale

- This option is incorrect because spreading related functionality across the system weakens
  cohesion.
- Correct. If related functionality is spread across the system, it means that the system has weak
  cohesion.
- This option is incorrect because even if related functionality is spread across the system, there
  is still some level of cohesion, albeit weak.

# Formative

Microservices and Coupling

## Question

What is the main advantage of having loosely coupled services in a microservice architecture?

- Being able to make a change to one service and deploy it without needing to change any other part
  of the system.
- [ ] Being able to make a change to one service and deploy it only after changing all other parts of
      the system.
- [ ] Being able to make a change to one service and deploy it while requiring changes to some other
      parts of the system.

### Rationale

- Correct. The main advantage of loosely coupled services is the ability to change and deploy one
  service independently of others.
- This is incorrect. The goal of loosely coupled services is to avoid the need for changes in all
  other parts of the system when one service is changed.
- This is incorrect. The goal of loosely coupled services is to avoid the need for changes in any
  other parts of the system when one service is changed.

## Question

What is a common mistake that can lead to tight coupling in microservices?

- [ ] Limiting the number of different types of calls from one service to another.
- Choosing an integration style that tightly binds one service to another.
- [ ] Making a service know as little as it needs to about the services with which it collaborates.

### Rationale

- This is incorrect. Limiting the number of different types of calls from one service to another can
  actually help prevent tight coupling.
- Correct. Choosing an integration style that tightly binds one service to another can lead to tight
  coupling, as changes inside the service may require changes to consumers.
- This is incorrect. Making a service know as little as it needs to about the services with which it
  collaborates is a characteristic of loosely coupled services, not a mistake that leads to tight
  coupling.

## Question

Why might it be beneficial to limit the number of different types of calls from one service to
another in a microservice architecture?

- It can help prevent tight coupling and potential performance problems.
- [ ] It can help increase the complexity of the system.
- [ ] It can help ensure that all services are tightly bound to each other.

### Rationale

- Correct. Limiting the number of different types of calls from one service to another can help
  prevent tight coupling and potential performance problems.
- This is incorrect. The goal of limiting the number of different types of calls from one service to
  another is

# Formative

Microservices Design Principles

## Question

What is the relationship between coupling and cohesion in the context of microservices?

- Cohesion applies to the relationship between things inside a microservice, whereas coupling
  describes the relationship between things across a microservice.
- [ ] Cohesion describes the relationship between different microservices, whereas coupling applies
      to the relationship between things inside a microservice.
- [ ] Cohesion and coupling are unrelated concepts in the context of microservices.
- [ ] Cohesion and coupling both describe the relationship between different microservices.

### Rationale

- Correct. Cohesion refers to how closely the responsibilities of a single module (in this case, a
  microservice) are related to each other, while coupling refers to how much a module depends on the
  details of another module.
- This is the opposite of the correct answer. Cohesion applies to the relationship within a
  microservice, while coupling describes the relationship between microservices.
- Cohesion and coupling are closely related concepts in the context of microservices, and
  understanding them is crucial to designing effective microservices.
- Cohesion applies to the relationship within a microservice, while coupling describes the
  relationship between microservices.

## Question

What does Constantine's law state about the stability of a structure in the context of microservices?

- [ ] A structure is stable if cohesion is low and coupling is strong.
- A structure is stable if cohesion is strong and coupling is low.
- [ ] A structure is stable if both cohesion and coupling are low.
- [ ] A structure is stable if both cohesion and coupling are high.

### Rationale

- This is the opposite of Constantine's law. A structure is more stable when cohesion is high and
  coupling is low.
- Correct. Constantine's law states that a structure is stable if cohesion is strong and coupling is
  low.
- While low coupling is desirable for stability, low cohesion is not. High cohesion means that
  related functionalities are grouped together, which contributes to stability.
- High coupling can lead to instability as changes in one module may affect another. Therefore, a
  structure with high cohesion and low coupling is considered more stable.

## Question

Why is it important to find the right balance between coupling and cohesion in microservices?

- To ensure independent deployability and reduce the amount of coordination between teams working on
  these services.
- [ ] To ensure that all microservices are identical in structure and functionality

# Formative

Microservices and Coupling

## Question

Is all coupling in a system considered bad?

- No
- [ ] Yes

### Rationale

- Correct. While it's desirable to reduce coupling, some amount of it is unavoidable in a system.
- This is incorrect. Some coupling in a system is unavoidable, and the goal is to reduce it, not
  eliminate it completely.

## Question

In the context of microservices, can the original concepts of coupling from structured programming be
applied?

- Yes
- [ ] No

### Rationale

- Correct. Microservices are a style of modular architecture, and the original concepts of coupling
  from structured programming can be applied, albeit with the added complexity of distributed systems.
- This is incorrect. Despite the added complexity of distributed systems, the original concepts of
  coupling from structured programming can still be applied to microservices.

# Summative

Understanding Coupling in Microservices

## Question

What is the primary goal when dealing with coupling in a system?

- [ ] To eliminate all coupling
- To reduce the amount of coupling
- [ ] To increase the amount of coupling

### Rationale

- This is incorrect. It's not possible to eliminate all coupling in a system.
- Correct. The primary goal is to reduce the amount of coupling in a system.
- This is incorrect. Increasing the amount of coupling in a system would lead to more dependencies
  and potential issues.

## Question

What is the relationship between microservices and structured programming in the context of coupling?

- [ ] They are completely unrelated
- Microservices can apply the original concepts of coupling from structured programming
- [ ] Structured programming cannot provide any insights for microservices

### Rationale

- This is incorrect. Microservices and structured programming are related in the context of coupling.
- Correct. Microservices, as a style of modular architecture, can apply the original concepts of
  coupling from structured programming, despite the added complexity of distributed systems.
- This is incorrect. Structured programming, particularly its original concepts of coupling, can
  provide valuable insights for microservices.

# Formative

Microservices and Structured Programming

## Question

Who are the authors of the book "Structured Design", which is considered one of the most important
texts in the area of structured programming?

- Larry Constantine and Edward Yourdon
- [ ] Meilir Page-Jones
- [ ] Edward Yourdon and Meilir Page-Jones

### Rationale

- Correct. Larry Constantine and Edward Yourdon are the authors of "Structured Design".
- Meilir Page-Jones is the author of "The Practical Guide to Structured Systems Design", not
  "Structured Design".
- Edward Yourdon co-authored "Structured Design" with Larry Constantine, not Meilir Page-Jones.

## Question

In the context of microservices, how are the different types of coupling organized?

- [ ] From high (desirable) to low (undesirable)
- From low (desirable) to high (undesirable)
- [ ] There is no specific organization for the types of coupling

### Rationale

- Incorrect. In the context of microservices, coupling is organized from low (desirable) to high
  (undesirable), not the other way around.
- Correct. The different types of coupling are organized from low (desirable) to high (undesirable).
- Incorrect. The text clearly states that the types of coupling are organized from low (desirable) to
  high (undesirable).

## Question

What is the author's approach when the ideas do not map cleanly to the different types of coupling
for microservices?

- [ ] The author discards those ideas
- [ ] The author sticks with the previous definitions
- The author synthesizes a working model, comes up with new terms or blends in ideas from elsewhere

### Rationale

- Incorrect. The author does not discard the ideas that do not map cleanly. Instead, he synthesizes a
  working model, comes up with new terms or blends in ideas from elsewhere.
- Incorrect. The author sticks with the previous definitions only when the ideas map cleanly to them.
- Correct. When the ideas do not map cleanly to the different types of coupling for microservices,
  the author synthesizes a working model, comes up with new terms or blends in ideas from elsewhere.

# Formative

Microservices and Domain Coupling

## Question

In the context of microservices, what does domain coupling refer to?

- A situation where one microservice interacts with another to utilize its functionality.
- [ ] A situation where a microservice is dependent on a database.
- [ ] A situation where a microservice is tightly coupled with the user interface.

### Rationale

- Correct. Domain coupling refers to a situation where one microservice needs to interact with
  another to make use of its functionality.
- A microservice's dependency on a database is not referred to as domain coupling.
- The coupling of a microservice with the user interface is not referred to as domain coupling.

## Question

In the MusicCorp example, which microservice is dependent on, and coupled to, the `Warehouse` and
`Payment` microservices?

- [ ] `Warehouse`
- [ ] `Payment`
- `Order Processor`

### Rationale

- The `Warehouse` microservice is not dependent on any other microservice in this example.
- The `Payment` microservice is not dependent on any other microservice in this example.
- Correct. The `Order Processor` microservice is dependent on, and coupled to, the `Warehouse` and
  `Payment` microservices.

## Question

What can be a potential issue with a single microservice depending on multiple downstream services?

- It might imply a microservice that is doing too much.
- [ ] It might imply that the microservice is not needed.
- [ ] It might imply that the microservice is not functioning properly.

### Rationale

- Correct. A single microservice depending on multiple downstream services might imply that the
  microservice is doing too much.
- A microservice depending on multiple downstream services does not necessarily imply that the
  microservice is not needed.
- A microservice depending on multiple downstream services does not necessarily imply that the
  microservice is not functioning properly.

# Formative

Microservices and Temporal Coupling

## Question

What is temporal coupling in the context of a distributed system?

- [ ] A situation where one microservice needs to be updated at the same time as another.
- A situation where one microservice needs another microservice to do something at the same time for
  the operation to complete.
- [ ] A situation where one microservice needs to be developed at the same time as another.

### Rationale

- Temporal coupling does not refer to the timing of updates.
- Correct. In a distributed system, temporal coupling refers to the need for simultaneous operation
  of microservices for a task to complete.
- Temporal coupling does not refer to the timing of development.

## Question

What can be a potential issue with temporal coupling in a distributed system?

- [ ] It can lead to unnecessary code duplication.
- It can cause resource contention if one microservice has to block and wait for a response from
  another.
- [ ] It can lead to a lack of cohesion between microservices.

### Rationale

- Temporal coupling does not directly lead to code duplication.
- Correct. If one microservice has to wait for another to complete its operation, it can lead to
  resource contention.
- Lack of cohesion is not directly related to temporal coupling.

## Question

What is one way to avoid temporal coupling in a distributed system?

- [ ] By using synchronous communication.
- By using some form of asynchronous communication, such as a message broker.
- [ ] By using a single, monolithic system instead of microservices.

### Rationale

- Synchronous communication can actually increase temporal coupling, as it requires microservices to
  operate simultaneously.
- Correct. Asynchronous communication allows microservices to operate independently of each other,
  reducing temporal coupling.
- Using a monolithic system does not necessarily avoid temporal coupling, and it introduces other
  potential issues.

# Formative

Microservices and Pass-Through Coupling

## Question

What is pass-through coupling in the context of microservices?

- [ ] It is when a microservice passes data to another microservice because the data is needed by the
      first microservice.
- It is when a microservice passes data to another microservice purely because the data is needed by
  some other microservice further downstream.
- [ ] It is when a microservice passes data to another microservice because the data is not needed by
      any other microservice.

### Rationale

- This is incorrect. Pass-through coupling is not about data needed by the first microservice.
- Correct. Pass-through coupling describes a situation where one microservice passes data to another
  because the data is needed by a third microservice further downstream.
- This is incorrect. Pass-through coupling is about data needed by a third microservice, not about
  data that is not needed by any other microservice.

## Question

What is a potential issue with pass-through coupling?

- [ ] It reduces the complexity of the system.
- A change to the required data downstream can cause a more significant upstream change.
- [ ] It increases the efficiency of data transfer between microservices.

### Rationale

- This is incorrect. Pass-through coupling does not reduce the complexity of the system. In fact, it
  can increase it.
- Correct. A change to the required data downstream can cause a more significant upstream change,
  which can increase complexity and make the system harder to maintain.
- This is incorrect. Pass-through coupling does not necessarily increase the efficiency of data
  transfer between microservices.

## Question

What is one way to mitigate the issues caused by pass-through coupling?

- [ ] Increase the amount of data passed between microservices.
- Have the intermediary microservice construct the required data locally.
- [ ] Remove the intermediary microservice entirely.

### Rationale

- This is incorrect. Increasing the amount of data passed between microservices does not mitigate the
  issues caused by pass-through coupling.
- Correct. One way to mitigate the issues caused by pass-through coupling is to have the intermediary
  microservice construct the required data locally. This can help to hide changes in the service
  contract of the downstream microservice from the upstream microservice.
- This is incorrect. Removing the intermediary microservice entirely may not be feasible or
  desirable, and it does not necessarily mitigate the issues caused by pass-through coupling.

* After reading this text, the learner will be able to explain the concept of common coupling in
  microservices, including its potential impacts on system performance and data integrity.
* After reading this text, the learner will be able to identify potential solutions to mitigate the
  issues associated with common coupling, such as the use of a finite state machine or designating a
  single microservice to manage shared data.

# Formative

Microservices and Common Coupling

## Question

What is common coupling in the context of microservices?

- [ ] When two microservices are dependent on the same third-party service.
- When two or more microservices make use of a common set of data.
- [ ] When two microservices are developed by the same team.
- [ ] When two microservices are deployed on the same server.

### Rationale

- While dependency on a third-party service can introduce coupling, it is not what is referred to as
  common coupling.
- Correct. Common coupling refers to the scenario where multiple microservices are using the same set
  of data.
- The team developing the microservices does not influence the type of coupling.
- The deployment environment does not influence the type of coupling.

## Question

What is a potential issue with common coupling in microservices?

- [ ] It increases the complexity of individual microservices.
- [ ] It makes it difficult to scale individual microservices.
- Changes to the structure of the shared data can impact multiple microservices at once.
- [ ] It makes it difficult to deploy individual microservices.

### Rationale

- While complexity can be an issue in microservices, it is not a direct result of common coupling.
- Scaling individual microservices is not directly impacted by common coupling.
- Correct. Changes to the shared data can impact all microservices that are using it, making it
  difficult to manage changes.
- Deployment of individual microservices is not directly impacted by common coupling.

## Question

What is one way to manage the state of an entity in a system with common coupling?

- [ ] By using a shared database for all state changes.
- [ ] By allowing each microservice to manage its own state independently.
- By creating a finite state machine to manage the transition of the entity from one state to
  another.
- [ ] By using a centralized server to manage all state changes.

### Rationale

- A shared database can lead to more common coupling, which we are trying to avoid.
- Allowing each microservice to manage its own state independently can lead to inconsistencies.
- Correct. A finite state machine can ensure that invalid state transitions are prohibited, helping
  to manage the state of an entity in a system with common coupling.
- A centralized server can introduce a single point of failure and does not necessarily solve the
  problem of managing state in a system with common coupling.

# Formative

Microservices and Coupling

## Question

What is content coupling in the context of microservices?

- [ ] A situation where two or more microservices are reading and writing to the same set of data.
- A situation where an upstream service reaches into the internals of a downstream service and
  changes its internal state.
- [ ] A situation where a microservice is dependent on an external service for its functionality.
- [ ] A situation where a microservice shares its internal state with other microservices.

### Rationale

- This is a description of common coupling, not content coupling.
- Correct. Content coupling occurs when an upstream service directly accesses and changes the
  internal state of a downstream service.
- This is a description of a service dependency, not content coupling.
- This is a general description of service interaction, not content coupling.

## Question

What are the potential issues with content coupling in microservices?

- It blurs the lines of ownership and makes it difficult for developers to change a system.
- It exposes the internal data structure of a service to an outside party.
- It can lead to duplication of logic and inconsistent state changes.
- [ ] It makes it easier for developers to understand the dependencies between services.

### Rationale

- Correct. Content coupling can make it unclear who owns and controls certain data, making it harder
  to make changes.
- Correct. Content coupling can expose the internal data structure of a service, making it vulnerable
  to changes by outside parties.
- Correct. Content coupling can lead to duplication of logic and inconsistent state changes if
  different services have different rules for changing state.
- Incorrect. Content coupling actually makes it harder to understand dependencies because it blurs
  the lines of ownership and control.

## Question

What is a potential solution to avoid content coupling in microservices?

- [ ] Allow all services to access and change the internal state of all other services.
- [ ] Make all data structures public and accessible to all services.
- Have services send requests to other services, where the request can be vetted and the internal
  detail can be hidden.
- [ ] Make all services dependent on a central database.

### Rationale

- This would increase content coupling, not reduce it.
- This would increase content coupling, not reduce it.
- Correct. Having services send requests to other services allows for control over what changes can
  be made and hides internal details.

# Formative

Domain-Driven Design in Microservices

## Question

What is the primary mechanism used for finding microservice boundaries?

- [ ] Object-oriented programming languages
- Domain-driven design
- [ ] Information hiding
- [ ] Coupling and cohesion

### Rationale

- Object-oriented programming languages like Simula were developed to model real domains, but they
  are not the primary mechanism for finding microservice boundaries.
- Correct. Domain-driven design (DDD) is used to create a model of the domain and find microservice
  boundaries.
- Information hiding is a concept in microservices, but it is not the primary mechanism for finding
  microservice boundaries.
- Coupling and cohesion are important concepts in microservices, but they are not the primary
  mechanism for finding microservice boundaries.

## Question

What is the purpose of a ubiquitous language in domain-driven design?

- [ ] To manage objects as a single entity
- [ ] To provide functionality to the wider system
- To aid communication by defining and adopting a common language in code and in describing the
  domain
- [ ] To hide complexity within a business domain

### Rationale

- Managing objects as a single entity is the purpose of an aggregate in domain-driven design, not a
  ubiquitous language.
- Providing functionality to the wider system is the purpose of a bounded context in domain-driven
  design, not a ubiquitous language.
- Correct. A ubiquitous language in domain-driven design is used to aid communication by defining and
  adopting a common language in code and in describing the domain.
- Hiding complexity within a business domain is the purpose of a bounded context in domain-driven
  design, not a ubiquitous language.

## Question

What is the role of a bounded context in domain-driven design?

- [ ] To manage objects as a single entity
- To provide functionality to the wider system and hide complexity
- [ ] To aid communication by defining and adopting a common language in code and in describing the
      domain
- [ ] To find microservice boundaries

### Rationale

- Managing objects as a single entity is the purpose of an aggregate in domain-driven design, not a
  bounded context.
- Correct. A bounded context in domain-driven design provides functionality to the wider system and
  hides complexity.
- Aiding communication by defining and adopting a common language in code and in describing the
  domain is the purpose of a ubiquitous language in domain-driven design, not a bounded context.
- Finding microservice boundaries is done using

# Formative

Microservices and Domain-Driven Design

## Question

What does the term "Ubiquitous Language" refer to in the context of domain-driven design?

- The practice of using the same terms in code as the users use, to improve communication and model
  the real-world domain.
- [ ] The use of a standard data model for the database, such as the IBM banking model.
- [ ] The process of mapping the rich domain language of the product owner to the generic code
      concepts.
- [ ] The practice of using technical jargon in code to maintain a level of professionalism.

### Rationale

- Correct. Ubiquitous Language is about using the same terms in code as the users use, to improve
  communication and model the real-world domain.
- The IBM banking model is an example of a standard data model, not Ubiquitous Language.
- Mapping the rich domain language of the product owner to the generic code concepts is a problem
  that Ubiquitous Language aims to solve, not the definition of Ubiquitous Language itself.
- Using technical jargon in code can actually hinder communication and understanding, which is the
  opposite of what Ubiquitous Language aims to achieve.

## Question

What are some potential issues that can arise when the code does not use the same language as the
users?

- It can make it harder to model the real-world domain.
- It can lead to a lot of work in helping translate between the domain language and the code
  concepts.
- It can result in business analysts spending their time explaining the same concepts over and over
  again.
- [ ] It can make the code more efficient and easier to understand.

### Rationale

- Correct. If the code does not use the same language as the users, it can make it harder to model
  the real-world domain.
- Correct. If the code does not use the same language as the users, it can lead to a lot of work in
  helping translate between the domain language and the code concepts.
- Correct. If the code does not use the same language as the users, it can result in business
  analysts spending their time explaining the same concepts over and over again.
- Incorrect. If the code does not use the same language as the users, it can actually make the code
  more difficult to understand, not easier.

# Formative

Microservices and Domain-Driven Design

## Question

In Domain-Driven Design (DDD), what is an aggregate and how is it typically represented?

- [ ] An aggregate is a collection of unrelated objects that are grouped together for convenience.
- An aggregate is a representation of a real domain concept, such as an Order or an Invoice, and
  typically has a life cycle around it.
- [ ] An aggregate is a database unit that is used to store and manage data.
- [ ] An aggregate is a type of microservice that handles multiple related tasks.

### Rationale

- An aggregate is not just a random collection of objects. It represents a real domain concept and
  has a life cycle.
- Correct. An aggregate represents a real domain concept and typically has a life cycle around it.
- While an aggregate may involve data storage and management, it is not a database unit. It is a
  concept in Domain-Driven Design.
- An aggregate is a concept in Domain-Driven Design, not a type of microservice.

## Question

How should an aggregate be managed in the context of microservices?

- [ ] An aggregate should be managed by multiple microservices to ensure redundancy.
- An aggregate should be managed by one microservice, although a single microservice might own
  management of multiple aggregates.
- [ ] An aggregate should not be managed by any microservice. It should be independent.
- [ ] An aggregate should be managed by a central microservice that handles all aggregates.

### Rationale

- Managing an aggregate with multiple microservices can lead to inconsistencies and conflicts. It is
  better to have one microservice manage an aggregate.
- Correct. An aggregate should be managed by one microservice, although a single microservice might
  own management of multiple aggregates.
- An aggregate needs to be managed by a microservice to handle its life cycle and state transitions.
- Having a central microservice handle all aggregates can lead to a monolithic architecture, which is
  contrary to the principles of microservices.

## Question

What is the key thing to understand about state transitions in an aggregate?

- [ ] State transitions in an aggregate can be requested by any outside party without restrictions.
- If an outside party requests a state transition in an aggregate, the aggregate can say no.
- [ ] State transitions in an aggregate are always initiated by the aggregate itself.
- [ ] State transitions in an aggregate are managed by a separate microservice.

# Formative

Microservices and Bounded Contexts

## Question

In the context of microservices, what is a bounded context?

- [ ] A specific type of microservice that handles data storage
- A larger organizational boundary within which explicit responsibilities are carried out
- [ ] A method for handling inter-service dependencies
- [ ] A technique for managing lookups in a shared model

### Rationale

- A bounded context is not a specific type of microservice.
- Correct. A bounded context represents a larger organizational boundary within which explicit
  responsibilities are carried out.
- While bounded contexts may have relationships with other bounded contexts, they are not a method
  for handling inter-service dependencies.
- Managing lookups in a shared model is a technique that can be used within a bounded context, but it
  is not what defines a bounded context.

## Question

What is the purpose of hiding internal details within a bounded context?

- To prevent unnecessary exposure of internal operations to the outside world
- [ ] To reduce the complexity of the microservice architecture
- [ ] To increase the efficiency of data storage and retrieval
- [ ] To facilitate inter-service communication

### Rationale

- Correct. Hiding internal details within a bounded context prevents unnecessary exposure of internal
  operations to the outside world.
- While hiding internal details can contribute to reducing complexity, it is not the primary purpose
  of doing so.
- Hiding internal details does not directly affect the efficiency of data storage and retrieval.
- Hiding internal details does not facilitate inter-service communication; it actually limits it to
  what is necessary.

## Question

In a situation where a shared model like a stock item has different meanings in different bounded
contexts, what might be a good approach?

- [ ] Use the same name for the shared model in all bounded contexts
- [ ] Avoid using shared models in different bounded contexts
- Use different names for the shared model in different bounded contexts, reflecting its role in
  each context
- [ ] Store all information about the shared model in a single, central location

### Rationale

- Using the same name for the shared model in all bounded contexts can lead to confusion, as the
  model may have different meanings in different contexts.
- Avoiding the use of shared models in different bounded contexts is not always feasible or
  desirable.
- Correct. Using different names for the shared model in different bounded contexts, reflecting its
  role in each context, can help

# Formative

Microservices and Domain-Driven Design

## Question

What is the relationship between aggregates, bounded contexts, and microservices in a system?

- [ ] Aggregates and bounded contexts are unrelated to microservices.
- [ ] One microservice should manage more than one aggregate.
- One microservice can manage one or more aggregates, but one aggregate should not be managed by
  more than one microservice.
- [ ] Bounded contexts should not be used as service boundaries.

### Rationale

- Aggregates and bounded contexts are foundational concepts in microservices and influence their
  design and boundaries.
- This would lead to issues with coupling and cohesion, as aggregates are meant to be self-contained.
- Correct. This maintains the integrity of the aggregate as a self-contained unit and allows for
  effective information hiding.
- Bounded contexts can work well as service boundaries and can encompass entire services.

## Question

What is the benefit of using a nested approach to bounded contexts in microservices?

- [ ] It allows for more complex service architectures.
- It simplifies testing and provides a unit of isolation for larger-scoped tests.
- [ ] It allows for more microservices to be created.
- [ ] It makes the system more dependent on individual microservices.

### Rationale

- While it may lead to more complex architectures, this is not a direct benefit of the nested
  approach.
- Correct. By chunking up the architecture, testing can be simplified and larger-scoped tests can be
  isolated.
- The number of microservices is not directly related to the use of a nested approach.
- The nested approach actually helps to isolate larger-scoped tests and can reduce dependencies.

## Question

What is the purpose of presenting a coarser-grained API to consumers when a service that models an
entire bounded context is split into smaller services?

- [ ] To make the system more complex.
- [ ] To increase the number of microservices.
- To hide the decision to decompose a service into smaller parts, which is an implementation detail.
- [ ] To make the system less efficient.

### Rationale

- The purpose is not to make the system more complex, but to hide implementation details.
- The number of microservices is not directly related to the presentation of a coarser-grained API.
- Correct. This is a form of information hiding, which can keep consumers unaware of changes in
  internal implementation.
- The

# Formative

Microservices and Event Storming

## Question

What is the primary purpose of the event storming technique in microservices?

- To collaboratively develop a shared domain model with both technical and non-technical
  stakeholders.
- [ ] To identify and mitigate potential issues related to different types of coupling in
      microservices.
- [ ] To apply alternative techniques to Domain-Driven Design for establishing microservice
      boundaries.

### Rationale

- Correct. Event storming is a collaborative brainstorming exercise designed to help surface a domain
  model with a shared, joined-up view of the world.
- Event storming does not directly deal with issues related to different types of coupling in
  microservices.
- While event storming can help in establishing microservice boundaries, it is not an alternative
  technique to Domain-Driven Design.

## Question

In the event storming process, what do the orange sticky notes represent?

- [ ] Commands
- [ ] Aggregates
- Domain events

### Rationale

- Commands are captured on blue sticky notes, not orange.
- Aggregates are represented by yellow sticky notes, not orange.
- Correct. Domain events, which represent things that happen in the system, are captured on orange
  sticky notes.

## Question

What is the role of aggregates in the event storming process?

- They represent potential entities in the system and help understand how different entities are
  related to each other.
- [ ] They represent the commands that cause domain events to happen.
- [ ] They represent the different parts of the organization that use the system.

### Rationale

- Correct. Aggregates are represented by yellow sticky notes, and the commands and events associated
  with that aggregate are moved and clustered around the aggregate. This also helps you understand how
  aggregates are related to each other.
- Commands are represented by blue sticky notes, not aggregates.
- Bounded contexts, not aggregates, most commonly follow a company’s organizational structure.

# Formative

Domain-Driven Design for Microservices

## Question

What is the role of bounded contexts in Domain-Driven Design (DDD) for microservices?

- [ ] Bounded contexts are used to define the physical boundaries of a microservice.
- Bounded contexts are used to hide internal complexity and present a clear boundary to the wider
  system.
- [ ] Bounded contexts are used to define the communication protocols between microservices.
- [ ] Bounded contexts are used to define the data storage mechanisms for a microservice.

### Rationale

- Bounded contexts are not about physical boundaries but about logical boundaries within the domain
  model.
- Correct. Bounded contexts in DDD are about hiding internal complexity and presenting a clear
  boundary to the wider system.
- Bounded contexts do not define communication protocols, but they can influence the design of APIs
  and event formats.
- Bounded contexts do not define data storage mechanisms, but they can influence the design of data
  models within a microservice.

## Question

How does the concept of a ubiquitous language contribute to the design of microservice endpoints in
Domain-Driven Design (DDD)?

- [ ] It provides a standardized programming language for all microservices.
- It provides a shared vocabulary for defining APIs, event formats, and other interfaces.
- [ ] It provides a common language for documenting microservices.
- [ ] It provides a language for defining the business logic within a microservice.

### Rationale

- A ubiquitous language is not about programming languages, but about the language used to describe
  the domain model.
- Correct. A ubiquitous language provides a shared vocabulary for defining APIs, event formats, and
  other interfaces.
- A ubiquitous language is not primarily about documentation, although it can help improve the
  clarity of documentation.
- A ubiquitous language is not about defining business logic, but it can help improve the clarity and
  consistency of business logic.

## Question

How does Domain-Driven Design (DDD) help align the technical architecture with the wider
organizational structure?

- [ ] By enforcing a strict hierarchy of microservices that mirrors the organizational structure.
- By encouraging the use of business language in code and service design, which improves domain
  expertise and communication among technical delivery, product development, and end users.
- [ ] By requiring all microservices to be designed and implemented by a single team.
- [ ] By mandating the use of a specific technology stack across all microservices.

### R

# Formative

Microservices and Domain-Driven Design

## Question

Which of the following is true about Domain-Driven Design (DDD) in the context of microservices?

- [ ] DDD is the only technique to consider when finding microservice boundaries.
- DDD can be used in conjunction with other methods to identify how a system should be split.
- [ ] DDD is not useful when building microservice architectures.

### Rationale

- This is incorrect. The text clearly states that it would be a mistake to consider DDD as the only
  technique when finding microservice boundaries.
- Correct. The text mentions that DDD can be used along with other methods to identify how (and if) a
  system should be split.
- This is incorrect. The text states that DDD can be incredibly useful when building microservice
  architectures.

## Question

What is the role of Domain-Driven Design (DDD) in establishing microservice boundaries?

- It helps in identifying how a system should be split.
- [ ] It helps in identifying the technology stack for microservices.
- [ ] It helps in identifying the number of microservices needed.

### Rationale

- Correct. The text mentions that DDD can be used to identify how (and if) a system should be split.
- This is incorrect. The text does not mention anything about DDD helping in identifying the
  technology stack for microservices.
- This is incorrect. The text does not mention anything about DDD helping in identifying the number
  of microservices needed.

# Summative

Microservices and Alternative Techniques

## Question

What is the importance of considering alternative techniques to Domain-Driven Design (DDD) when
finding microservice boundaries?

- It allows for a more flexible and comprehensive approach to system decomposition.
- [ ] It reduces the complexity of the system.
- [ ] It eliminates the need for DDD.

### Rationale

- Correct. Considering alternative techniques to DDD when finding microservice boundaries allows for
  a more flexible and comprehensive approach to system decomposition.
- This is incorrect. The text does not mention anything about alternative techniques reducing the
  complexity of the system.
- This is incorrect. The text does not suggest that alternative techniques eliminate the need for
  DDD. Instead, it suggests using them in conjunction with DDD.

# Formative

Microservices and Volatility-Based Decomposition

## Question

What is the main principle behind volatility-based decomposition in microservices?

- Identifying parts of the system that undergo frequent changes and extracting them into their own
  services.
- [ ] Breaking down the system based on the complexity of its components.
- [ ] Dividing the system based on the size of its components.
- [ ] Separating the system into different services based on their dependencies.

### Rationale

- Correct. Volatility-based decomposition involves identifying parts of the system that change
  frequently and extracting them into their own services.
- Complexity is not the primary factor in volatility-based decomposition.
- Size is not the primary factor in volatility-based decomposition.
- Dependencies may play a role in decomposition, but they are not the primary factor in
  volatility-based decomposition.

## Question

What is the concept of bimodal IT as put forward by Gartner?

- [ ] A model that categorizes systems based on their size and complexity.
- A model that categorizes systems into "Mode 1" (Systems of Record) and "Mode 2" (Systems of
  Innovation) based on their rate of change and business involvement.
- [ ] A model that categorizes systems based on their dependencies and coupling.
- [ ] A model that categorizes systems based on their technological stack.

### Rationale

- Bimodal IT is not about size and complexity.
- Correct. Bimodal IT categorizes systems into "Mode 1" (slow-changing, less business involvement)
  and "Mode 2" (fast-changing, high business involvement).
- Bimodal IT is not about dependencies and coupling.
- Bimodal IT is not about the technological stack.

## Question

Why does the author dislike the concept of bimodal IT?

- [ ] Because it is too complex to implement.
- Because it oversimplifies the system and can be used as an excuse to avoid dealing with difficult
  changes.
- [ ] Because it does not consider the size and complexity of the system.
- [ ] Because it does not take into account the technological stack of the system.

### Rationale

- The author does not mention complexity of implementation as a reason for disliking bimodal IT.
- Correct. The author criticizes bimodal IT for oversimplifying the system and potentially being used
  as an excuse to avoid dealing with difficult changes.
-

# Formative

Microservices and Data Segregation

## Question

Why did PaymentCo decide to segregate its system into a "red zone" and a "green zone"?

- [ ] To improve system performance
- To limit the scope of PCI requirements
- [ ] To increase system complexity
- [ ] To facilitate easier system updates

### Rationale

- While system performance may be improved by certain forms of system segregation, the text does not
  mention this as a reason for PaymentCo's decision.
- Correct. The text states that PaymentCo segregated its system to limit the scope of PCI
  requirements, reducing the parts of the system that needed to be audited.
- Increasing system complexity is generally not a goal of system design.
- While system updates may be easier with certain forms of system segregation, the text does not
  mention this as a reason for PaymentCo's decision.

## Question

What would happen if credit card information flowed into the "green zone" in PaymentCo's system?

- [ ] The system would crash
- [ ] The system would perform better
- The clear lines of separation would break down
- [ ] The system would become more secure

### Rationale

- The text does not suggest that the system would crash if credit card information flowed into the
  green zone.
- The text does not suggest that the system would perform better if credit card information flowed
  into the green zone.
- Correct. The text states that if credit card information flowed into the green zone, the clear
  lines of separation would break down.
- The text does not suggest that the system would become more secure if credit card information
  flowed into the green zone.

## Question

What is the role of the gateway in PaymentCo's system?

- [ ] To store credit card information
- To divert calls to the appropriate services and zones
- [ ] To perform system updates
- [ ] To audit the system

### Rationale

- The text does not suggest that the gateway stores credit card information.
- Correct. The text states that the gateway diverts calls to the appropriate services and zones.
- The text does not suggest that the gateway performs system updates.
- The text does not suggest that the gateway audits the system.

# Formative

Microservices and Technology

## Question

Why might the need to use different technology be a factor in determining the boundary of a
microservice?

- [ ] To accommodate different databases in a single running microservice.
- To accommodate different runtime models that may pose a challenge.
- [ ] To implement all functionality in a language like Rust for performance improvements.

### Rationale

- While different databases can be accommodated in a single microservice, this is not the primary
  reason for determining the boundary.
- Correct. If different parts of your functionality require different runtime models, this can pose a
  challenge and thus influence the boundary of a microservice.
- While Rust can provide performance improvements, it is not necessary to implement all functionality
  in Rust. The need for different technologies, not just Rust, can influence the boundary of a
  microservice.

## Question

What is a potential downside of using technology as a general means of decomposition in
microservices?

- It can lead to less than ideal architectures, such as the classic three-tiered architecture.
- [ ] It can lead to the inability to accommodate different databases in a single running
      microservice.
- [ ] It can prevent the use of languages like Rust for performance improvements.

### Rationale

- Correct. Grouping related technology together, as in the classic three-tiered architecture, can
  lead to less than ideal architectures.
- Accommodating different databases in a single microservice is not a downside of using technology as
  a means of decomposition.
- The use of different technologies, including languages like Rust, is a reason for decomposition,
  not a downside of it.

# Summative

Microservices and Technology

## Question

What is a major forcing factor in determining the boundary of a microservice?

- [ ] The need to use the same runtime model across the entire microservice.
- The need to implement part of your functionality in a different language for performance
  improvements.
- [ ] The need to use a three-tiered architecture.

### Rationale

- Using the same runtime model across the entire microservice is not a major forcing factor in
  determining the boundary.
- Correct. If part of your functionality needs to be implemented in a different language for
  performance improvements, this can be a major forcing factor in determining the boundary of a
  microservice.
- Using a three-tiered architecture is not a major forcing factor in determining the boundary. In
  fact, it can lead to less than

# Formative

Microservices and Organizational Structure

## Question

According to Conway's law, how does organizational structure influence system architecture?

- The organizational structure drives the system architecture.
- [ ] The system architecture drives the organizational structure.
- [ ] The organizational structure and system architecture are unrelated.
- [ ] The organizational structure and system architecture influence each other equally.

### Rationale

- Correct. The text states that "How you organize yourself ends up driving your systems
  architecture."
- The text does not suggest that system architecture drives organizational structure.
- The text clearly states that there is an interplay between organizational structure and system
  architecture.
- While there is an interplay between the two, the text suggests that the organizational structure
  has a stronger influence on system architecture.

## Question

What might happen if an organizational structure changes in relation to microservices?

- [ ] The microservices will remain unaffected.
- An existing microservice might need to be split.
- The owner of an existing microservice might change.
- [ ] The microservices will need to be completely redesigned.

### Rationale

- The text suggests that changes in organizational structure can affect microservices.
- Correct. The text states that "in the worst case, it might cause us to examine an existing
  microservice that now needs to be split."
- Correct. The text provides an example where "organizational changes would just require that the
  owner of an existing microservice changes."
- The text does not suggest that a complete redesign of microservices is necessary when
  organizational structure changes.

## Question

What was the issue with the service boundary split across technical seams in the case of the
California company?

- [ ] The services were not chatty enough.
- [ ] The services were not split along geographical lines.
- Changes frequently had to be made to both services.
- The service interface was overly brittle and chatty, leading to performance issues.

### Rationale

- The text does not suggest that the services were not chatty enough. In fact, it states that the
  service interface was very chatty, leading to performance issues.
- The services were split along geographical lines, but the issue was that they were not split along
  business-focused lines.
- Correct. The text states that "Changes frequently had to be made to both services."
- Correct. The text states that "The service interface was very chatty as well, resulting in
  performance issues."

# Formative

Microservices Architecture

## Question

What is the issue with using layering as the mechanism by which your microservice and ownership
boundaries are drawn?

- [ ] It makes the code harder to manage.
- It can lead to problems in the microservice architecture.
- [ ] It reduces the efficiency of the microservice.

### Rationale

- Incorrect. The text does not suggest that layering makes code harder to manage. In fact, it states
  that layering within a microservice boundary can make the code easier to manage.
- Correct. The text suggests that problems can occur when layering becomes the mechanism by which
  microservice and ownership boundaries are drawn.
- Incorrect. The text does not mention anything about the efficiency of the microservice.

## Question

Where can layering be beneficial in a microservice architecture?

- Within a microservice boundary
- [ ] Between microservice boundaries
- [ ] In the horizontal architecture

### Rationale

- Correct. The text states that within a microservice boundary, it can be sensible to delineate
  between different layers to make the code easier to manage.
- Incorrect. The text does not suggest that layering is beneficial between microservice boundaries.
- Incorrect. The text specifically states that the author is not a fan of horizontally layered
  architecture.

# Summative

Microservices Design

## Question

What is the author's stance on horizontally layered architecture in microservices?

- [ ] The author is a fan of horizontally layered architecture.
- The author is not a fan of horizontally layered architecture.
- [ ] The author has no opinion on horizontally layered architecture.

### Rationale

- Incorrect. The text clearly states that the author is not a fan of horizontally layered
  architecture.
- Correct. The text clearly states that the author is not a fan of horizontally layered architecture.
- Incorrect. The author clearly expresses an opinion on horizontally layered architecture, stating
  that they are not a fan.

# Formative

Microservices and Domain-Driven Design

## Question

What are some potential pitfalls of defining microservice boundaries without considering the
principles of information hiding, coupling, and cohesion?

- Poorly defined boundaries leading to inefficient microservices
- Increased complexity due to unnecessary interdependencies
- [ ] Faster delivery speed
- [ ] Reduced need for domain-oriented architecture

### Rationale

- Correct. Ignoring these principles can lead to poorly defined boundaries, which can make
  microservices inefficient.
- Correct. Ignoring these principles can lead to unnecessary interdependencies, which can increase
  complexity.
- Faster delivery speed is generally a benefit, not a pitfall.
- A reduced need for domain-oriented architecture is not a pitfall of ignoring these principles.

## Question

What factors might influence the decision to decompose a service further along technical lines?

- [ ] The service does not cross organizational boundaries
- [ ] The service is implemented in a single programming language
- Different parts of the service need to be implemented in different programming languages
- [ ] The service is not domain-oriented

### Rationale

- Services that do not cross organizational boundaries may not need to be decomposed further along
  technical lines.
- Services implemented in a single programming language may not need to be decomposed further along
  technical lines.
- Correct. If different parts of a service need to be implemented in different programming languages,
  it may be necessary to decompose the service further along technical lines.
- Whether or not a service is domain-oriented does not necessarily influence the decision to
  decompose it further along technical lines.

## Question

What is the main takeaway from the author's discussion on defining microservice boundaries?

- [ ] There is only one correct way to define microservice boundaries
- It's important to consider multiple factors and avoid dogmatic thinking
- [ ] Domain-oriented architecture is always the best choice
- [ ] Technical considerations should be the primary factor in defining boundaries

### Rationale

- The author explicitly states that there is not only one correct way to define microservice
  boundaries.
- Correct. The author emphasizes the importance of considering multiple factors and avoiding dogmatic
  thinking when defining microservice boundaries.
- The author does not claim that domain-oriented architecture is always the best choice.
- The author does not suggest that technical considerations should be the primary factor in defining
  boundaries.
