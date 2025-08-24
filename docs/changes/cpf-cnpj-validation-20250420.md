# Change: Brazilian Identifier Validation Implementation

**Date:** 2023-07-14

## Files Modified
- `src/schemas/clients.py`
- `tests/conftest.py`
- `tests/routes/test_clients.py`
- `tests/routes/test_token.py`
- `tests/schemas/test_client_validation.py` (new file)
- `docs/client_identifier_validation.md` (new file)

## Summary of Changes
Added validation for Brazilian CPF and CNPJ identifiers in the client management portion of the application. The validation ensures that CPF identifiers are exactly 11 digits long and CNPJ identifiers are exactly 14 digits long.

## Detailed Explanation
1. Added constants `CPF_LENGTH` (11) and `CNPJ_LENGTH` (14) to make the code more maintainable
2. Implemented a Pydantic field validator for the `identifier` field in the `ClientRequestCreate` model that checks the length of the identifier based on the selected type
3. Implemented a similar validator for the `ClientRequestUpdate` model with additional logic to handle partial updates
4. Updated test fixtures and test cases to use valid identifiers
5. Added unit tests specifically for the validation logic
6. Added documentation for the feature

## Potential Impacts
- Attempting to create or update a client with an invalid CPF or CNPJ length will now result in a validation error
- All client creation and update operations must now comply with the Brazilian standards for identifier lengths
- No impact on existing data as this is a validation-only change

## Future Considerations
In the future, we may want to enhance the validation to:
1. Ensure identifiers contain only digits
2. Implement checksum validation based on official Brazilian algorithms
3. Add optional formatting support for identifiers with or without punctuation 