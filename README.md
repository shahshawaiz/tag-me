# Introduction
TagMe is an end-to-end pipeline for object recognition requests with a Rest API interface. It can be thought as a basic version of Google Vision Cloud API.

Following project was completed in two milestones;
- Milestone 1:
Development of an object labelling routine. **Tensor flow&#39;s object detection API** was used for this purpose
- Milestone 2:
A Restful API interface for handling HTTP requests. API endpoints were developed using. Flask Restful (an extension of project Flask)

# UML
Following are the UML diagrams of project TagMe.

1.Activity Diagram
![Activity](https://raw.githubusercontent.com/shahshawaiz/tag-me/master/doc/images/activity-diagrams.PNG)

2.Use Case Diagram
![Use Case](https://raw.githubusercontent.com/shahshawaiz/tag-me/master/doc/images/Project%20-%20Use%20Case.jpg)

3.Deployment Diagram
![Deployment](https://raw.githubusercontent.com/shahshawaiz/tag-me/master/doc/images/deployment%20diag..jpg)

# Metrics
For the code analysis and review, the industry standard tool, &quot;SonarQube&quot; was used. Initially code smell was significantly higher, which was gradually mitigated by applying refactoring techniques.

Please note that during code analysis, source codes from 3rd party libraries (e.g. object detection module from TensorFlow) were excluded.

For Example;
- In one case, a large code block was broken down into smaller code blocks, hence reducing code complexity.
- Function parameters were increased/decreased for making method calls more simpler and easier.
- Logically related pieces of code were merged together under same functions.

Software metrics that were monitor during course of development were;

1.Complexity Metrics
In post-development code analysis, SonarQube indicated presence of Cyclomatic Complexity with a score of 17.

![Complexity Score](https://raw.githubusercontent.com/shahshawaiz/tag-me/master/doc/images/complexity.PNG)

Cyclomatic Complexity measures the minimum number of test cases required for full test coverage. Following measure indicates that my project requires 17 additional test cases for getting full test coverage.

2.Architectural Metrics
Following are screenshots from metric measures.

![Size](https://raw.githubusercontent.com/shahshawaiz/tag-me/master/doc/images/size.PNG)


# Clean Code Development

1.Consistent naming convention
Throughout coding, naming scheme of camel case is used for both variables and functions. Moreover, for immutable/final variables all-upper-casing scheme is used.

2.Minimizing of Side-Effect using Context Management
Wherever necessary, side-effects have been tried to minimized by isolating its effect at local scope by making use of python&#39;s context management.

![Context Management Usage](https://raw.githubusercontent.com/shahshawaiz/tag-me/master/doc/images/context-maagement.PNG)

3.Modularity

Source code has been divided into two modules. Module &quot;Analyzer&quot; is responsible for object recognition tasks, while module &quot;Router&quot; is responsible for routing of incoming and outgoing rest API requests.

![Modularity](https://raw.githubusercontent.com/shahshawaiz/tag-me/master/doc/images/modularity.PNG)

Module Analyzer(analyzer.py) being imported in Module Router(app.py)

1. 4.Exception Handling

Wherever necessary exception handling blocks have been added to ensure that no runtime errors are thrown.

(image)

Exception Handling Usage

1. 5.Configurable Data at Higher Level

All configurable data (for example: Directory names, paths), have been placed at higher level, making tweaking of values easier for the purpose of debugging.

(image)

Configurable Data and Constants at higher level

# Continuous Delivery

Continuous Delivery and integration pipeline of this project is based on Git, Travis CI and Heroku. Travis CI is listening for modifications on Git repository. Any modifications in code base will trigger Travis CI, which will initiate a set of tests for validating successful integration of newly added code with already tested production-ready code in Git repository. Upon successful integration, Travis CI will deploy source code on our production server at Heroku.

Following diagram depicts code delivery flow;

(image)

# Build Management (+ DSL)

For the purposes of build management this project is dependent on Travis CI since builds are being managed at the time of project deployment. Consider following example;

(image)

Build Script for Travis CI

During build deployment, Travis has been instructed to;

1. Check for compatibility of source code with python version 2.7, 3.4 and 3.5
2. Install pre-requisite packages of project found in file requirments.txt
3. Delete contents of directory &quot;images&quot; where images that are to be processed will be stored
4. Deploy fresh build on Heroku instance for application &quot;tag-me&quot; (unique identifier on Heroku.com)

Following is the output of following script;

(image)

Build Script Output Log Part 1

(image)

 Build Script Output Log Part 1

**P.S: Following script is also an example of Domain Specific Language. This script has been written in YAML (****.yml).**

# Functional Programming

Throughout this project, good practices for functional programming have been adopted. Following are few examples of such practices;

1. 1.Final Data Structures Usage

Few variables have been made made immutable in code. Hence using as constant.

(image)

2.Side Effect Free Functions

As discussed earlier, wherever necessary context management has been used. So that its effect could remain locally. Hence using them would not result any side effects.

(image)

3.Use of higher order functions

Higher order functions like map and filter have also been used.

(image)

4.Clojures/Anonymous Functions

Usage of anonymous functions like &quot;Lamda&quot; have also been made, for getting rid from unnecessary function signature bodies where required.

(image)