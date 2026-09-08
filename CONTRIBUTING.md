## Contributing to Fez / Transbot

Thank you for contributing to Fez / Transbot! Your efforts are greatly appreciated. Below are some guidelines for contributing.

By contributing to this project, you agree to release your contributions under the GNU Affero General Public License v3.0 (AGPL-3.0)

## Rules for Contributions

### 1. Do not use generative AI for any part of your contributions.
We reserve the right to deny any pull requests if we suspect AI has been used.

### 2. Do not open PRs for image, meme, or joke commands. 
They will not be accepted, and they will take valuable time away from the project's maintainers.  A maintainer will communicate with you in advance if a situation exists that allows for an exception to this policy.

### 3. Keep your contributions in scope of Fez / Transbot's purpose. 
Remember that they are moderation bots first and foremost, and any other features must serve a useful purpose. Contact a lead mod or admin if you are unsure if your idea would be in scope.

### 4. Keep the code style consistent
Follow the style guide, found below.

### 5. Keep Transpeak-specific code separated
If you are making a new feature specifically for Transpeak, think about whether a more general version could be made, then make separate code to use the general feature.
If you are making changes to an existing feature, ensure you are putting your changes in the correct place.

## Guide for contributing
1. Fork the repository
2. Create a new branch with a descriptive name
3. Make your changes
4. Open a pull request

## Style guide

### Names
We use snake_case (all lowercase, words are separated by underscores) for variables and functions, and PascalCase (capital letters at the beginning of each word, lowercase for the rest, no spaces) for classes and types.

### Object-Oriented Programming
We use Object-Oriented Programming for this project, which means all code is separated into different classes, which contain a set of variables and functions for a specific purpose. 

Ensure your class(es) contains only one purpose. If a class deals with more than one thing, you can likely separate it into multiple classes.

Keep global variables to an absolute minimum, as they pollute the namespace and make other code issues far more likely. Instead, use static and member variables within classes.

### Separation of concerns
Ensure that each of your functions does one thing and one thing only. If your function does a chain of things, separate it into multiple functions.

For example, a single function that takes a user's message, checks if it contains a command, has the logic for executing each of those commands, updates a database, sends message, etc. should be separated into multiple functions. 

A good example of separation of concerns is a function that receives the message, then it calls another function if it detects the command prefix that deals with executing commands, then it calls another function to update the user's message count in the database, etc. 