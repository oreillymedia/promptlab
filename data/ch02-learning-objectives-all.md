* After reading this text, the learner will be able to understand the foundational concepts of 
microservices such as information hiding, coupling, and cohesion, and how these concepts influence 
the design and boundaries of microservices.
* After reading this text, the learner will be able to explore different forms of decomposition and 
the role of domain-driven design in modeling microservices. 

* After reading this text, the learner will be able to understand the context and background of 
MusicCorp, including its transition from a brick-and-mortar retailer to an online retailer.
* After reading this text, the learner will be able to identify the company's strategy for adapting 
to changes in the music industry, specifically its decision to implement microservices. 

* After reading this text, the learner will be able to understand the importance of defining 
boundaries around microservices for independent deployment and changes.
* After reading this text, the learner will be able to explain the three key concepts vital for a 
good microservice boundary: information hiding, cohesion, and coupling. 

* After reading this text, the learner will be able to explain the concept of information hiding as 
developed by David Parnas and its relevance to defining module boundaries in microservice 
architectures.
* After reading this text, the learner will be able to describe the benefits of modules in terms of 
improved development time, comprehensibility, and flexibility, and how these characteristics are 
amplified in microservices.
* After reading this text, the learner will be able to discuss the importance of reducing the number 
of assumptions between modules or microservices to ensure safe changes and minimize impact on other 
modules. 

* After reading this text, the learner will be able to explain the concept of cohesion in the context
of microservice architecture, including its importance in optimizing changes in business 
functionality.
* After reading this text, the learner will be able to differentiate between strong and weak 
cohesion, and understand the implications of each on the efficiency and risk associated with changes 
in system behavior. 

* After reading this text, the learner will be able to explain the concept of coupling in a 
microservice architecture, including the difference between loose and tight coupling.
* After reading this text, the learner will be able to identify potential causes of tight coupling 
and discuss strategies to maintain loose coupling in a service-based architecture. 

* After reading this text, the learner will be able to explain the relationship between coupling and 
cohesion in the context of microservice boundaries and their impact on system stability.
* After reading this text, the learner will be able to discuss the trade-offs in organizing code with
respect to coupling and cohesion, and understand the need for revisiting these decisions as system 
requirements change. 

* After reading this text, the learner will be able to understand that not all coupling is bad and 
some level of it is unavoidable in systems.
* After reading this text, the learner will be able to explain how the concepts of coupling from 
structured programming can be applied to microservice-based systems. 

* After reading this text, the learner will be able to identify key texts in the field of structured 
programming and understand their importance in the development of microservices.
* After reading this text, the learner will be able to explain the concept of coupling in 
microservices, including the different types and their implications for microservice architecture. 

* After reading this text, the learner will be able to explain the concept of domain coupling in the 
context of microservices, including how it can become problematic when a single microservice depends 
on multiple downstream services.
* After reading this text, the learner will be able to discuss the importance of information hiding 
in mitigating issues related to domain coupling, emphasizing the need to share only necessary 
information and minimize data transmission. 

* After reading this text, the learner will be able to explain the concept of temporal coupling in 
both a code-centric view and in the context of a distributed system.
* After reading this text, the learner will be able to describe the potential issues that can arise 
from temporal coupling in a microservice architecture and suggest a method to avoid it, such as 
asynchronous communication. 

* After reading this text, the learner will be able to explain the concept of "pass-through coupling"
in the context of microservices, including its potential drawbacks and implications for system 
design.
* After reading this text, the learner will be able to describe different strategies for mitigating 
the issues associated with pass-through coupling, such as bypassing the intermediary microservice, 
hiding the requirement for certain data from the calling microservice, or treating certain data as a 
non-processed blob. 

* After reading this text, the learner will be able to explain the concept of common coupling in 
microservices, including its potential impacts on system performance and data integrity.
* After reading this text, the learner will be able to identify potential solutions to mitigate the 
issues associated with common coupling, such as the use of a finite state machine or designating a 
single microservice to manage shared data. 

* After reading this text, the learner will be able to explain the concept of content coupling and 
how it differs from common coupling, particularly in the context of microservices.
* After reading this text, the learner will be able to identify potential issues and risks associated
with content coupling, such as the loss of clear ownership and the difficulty in making system 
changes.
* After reading this text, the learner will be able to discuss the importance of maintaining a clear 
separation between what can be freely changed and what cannot in a microservice, and the potential 
consequences of not maintaining this separation.
* After reading this text, the learner will be able to propose solutions to avoid content coupling, 
such as having external services send requests to the appropriate service rather than directly 
accessing and changing another service's database. 

* After reading this text, the learner will be able to explain the role of domain-driven design in 
finding microservice boundaries.
* After reading this text, the learner will be able to define and describe the core concepts of 
domain-driven design, including ubiquitous language, aggregate, and bounded context. 

* After reading this text, the learner will be able to explain the concept of Ubiquitous Language and
its importance in improving communication between the delivery team and the actual people.
* After reading this text, the learner will be able to identify the potential issues that can arise 
when the code does not reflect the real-world language of the system being built, and how this can be
mitigated by incorporating the real-world language into the code. 

* After reading this text, the learner will be able to explain the concept of an aggregate in 
Domain-Driven Design (DDD), including its characteristics such as state, identity, and life cycle.
* After reading this text, the learner will be able to describe how aggregates are managed within 
microservices, including the handling of state transitions and relationships between different 
aggregates. 
* After reading this text, the learner will be able to discuss different methods for implementing 
relationships between aggregates across microservice boundaries, including the use of foreign keys 
and URIs. 
* After reading this text, the learner will be able to identify factors that may influence the design
and structure of aggregates within a system, such as user mental models and performance 
considerations. 

* After reading this text, the learner will be able to explain the concept of a bounded context and 
its role in an organization, including how it hides implementation details and contains one or more 
aggregates.
* After reading this text, the learner will be able to describe the relationship between different 
bounded contexts within an organization, using the example of the finance department and the 
warehouse in MusicCorp, and how they share models while maintaining their own internal details. 

* After reading this text, the learner will be able to understand the relationship between 
aggregates, bounded contexts, and microservices, and how they can be used as service boundaries.
* After reading this text, the learner will be able to comprehend the concept of nested bounded 
contexts and how they can be used to decompose larger services into smaller ones.
* After reading this text, the learner will be able to appreciate the importance of information 
hiding in microservices architecture and how it can simplify testing and provide isolation. 

* After reading this text, the learner will be able to explain the concept of Event Storming and its 
purpose in developing a shared domain model among technical and non-technical stakeholders.
* After reading this text, the learner will be able to describe the logistics of conducting an Event 
Storming session, including the importance of having all stakeholders present and the use of physical
tools like sticky notes and large rolls of paper.
* After reading this text, the learner will be able to outline the process of an Event Storming 
session, including the identification of domain events, commands, aggregates, and bounded contexts. 
* After reading this text, the learner will be able to discuss the potential challenges and 
disagreements that may arise during an Event Storming session, such as the availability of certain 
colored sticky notes or the physical demands of the session. 

* After reading this text, the learner will be able to explain the importance of Domain-Driven Design
(DDD) in the context of microservices, particularly its role in information hiding and finding stable
microservice boundaries.
* After reading this text, the learner will be able to describe how DDD's focus on a common, 
ubiquitous language aids in defining microservice endpoints and managing changes within bounded 
contexts.
* After reading this text, the learner will be able to discuss how DDD encourages the integration of 
business language into code and service design, fostering greater understanding and communication 
among technical delivery, product development, and end users. 

* After reading this text, the learner will be able to identify alternative techniques to 
Domain-Driven Design (DDD) for establishing microservice boundaries.
* After reading this text, the learner will be able to understand the importance of using multiple 
methods in conjunction with DDD for determining system splits. 

* After reading this text, the learner will be able to explain the concept of volatility-based 
decomposition and its potential benefits and drawbacks in system design.
* After reading this text, the learner will be able to critique the bimodal IT model, understanding 
its implications and potential pitfalls in a rapidly changing digital landscape. 

* After reading this text, the learner will be able to understand the importance of data segregation 
in systems handling sensitive information, such as credit card data, to comply with industry 
standards and reduce the risk of data breaches.
* After reading this text, the learner will be able to explain how system decomposition can be 
influenced by the nature of data a company handles, using the example of PaymentCo's strategy to 
limit the scope of PCI requirements. 

* After reading this text, the learner will be able to understand the challenges of accommodating 
different databases and runtime models in a single running microservice.
* After reading this text, the learner will be able to explain the implications of adopting 
technology-based decomposition as a general means, using the example of a three-tiered architecture. 

* After reading this text, the learner will be able to understand the interplay between 
organizational structure and system architecture, and how it influences the definition of service 
boundaries.
* After reading this text, the learner will be able to comprehend the implications of organizational 
changes on system architecture, and how to manage such changes effectively. 

* After reading this text, the learner will be able to distinguish between layering inside and 
outside of a microservice boundary.
* After reading this text, the learner will be able to explain why layering can become problematic 
when it defines microservice and ownership boundaries. 

* After reading this text, the learner will be able to understand the importance of flexibility in 
choosing mechanisms for defining microservice boundaries, and the potential pitfalls of adhering 
strictly to one method.
* After reading this text, the learner will be able to identify the factors that might influence 
their decisions in defining service boundaries, including the speed of delivery, organizational 
boundaries, and technical requirements. 

