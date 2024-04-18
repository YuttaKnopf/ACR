# Send emails secure function

This folder contains code that will be deployed to the function-app in Azure - the code receives an email address and sending address and the relevant details and activates a secure function for sending email.

## Dependencies

The following dependencies are required to run the code end deploy to function-app:

- azure-functions
- azure-cli
- azure-storage-blob
- azure-keyvault-secrets
- azure-identity
- python-dotenv
- requests
- msal

These dependencies exist in the 'requirements.txt' file.

## Running the code

The code is automatically run using CI CD processes through workflow.

## Tests

The code has undergone in-depth TEST tests with respect to end situations, the tests are also automatically run in the CI CD process through workflow.
