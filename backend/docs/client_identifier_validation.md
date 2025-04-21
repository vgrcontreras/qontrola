# Brazilian Identifier Validation Implementation

## Overview

This document describes the implementation of validation rules for Brazilian identification numbers (CPF and CNPJ) in the Studio Caju backend system.

## Background

In Brazil, individuals and businesses are identified by different types of identification numbers:

- **CPF (Cadastro de Pessoas Físicas)**: A tax identification number for individuals, consisting of exactly 11 digits.
- **CNPJ (Cadastro Nacional da Pessoa Jurídica)**: A tax identification number for businesses, consisting of exactly 14 digits.

## Implementation Details

### 1. Constants Definition

Constants have been defined to make the code more maintainable and clear:

```python
# Constants for identifier lengths
CPF_LENGTH = 11
CNPJ_LENGTH = 14
```

### 2. Validation in ClientRequestCreate Model

The `ClientRequestCreate` Pydantic model now includes validation for the `identifier` field based on the selected `type_identifier`:

```python
@field_validator('identifier')
def validate_identifier_length(cls, value, info):
    type_identifier = info.data.get('type_identifier')
    
    if (type_identifier == IdentifierType.cpf and 
            len(value) != CPF_LENGTH):
        raise ValueError('CPF must have exactly 11 digits')
    
    if (type_identifier == IdentifierType.cnpj and 
            len(value) != CNPJ_LENGTH):
        raise ValueError('CNPJ must have exactly 14 digits')
        
    return value
```

### 3. Validation in ClientRequestUpdate Model

Similar validation is implemented in the `ClientRequestUpdate` model, with additional checks to handle optional fields:

```python
@field_validator('identifier')
def validate_identifier_length(cls, value, info):
    if value is None:
        return value
        
    type_identifier = info.data.get('type_identifier')
    
    # If type_identifier is not provided in the update, we can't validate
    if type_identifier is None:
        return value
        
    if (type_identifier == IdentifierType.cpf and 
            len(value) != CPF_LENGTH):
        raise ValueError('CPF must have exactly 11 digits')
    
    if (type_identifier == IdentifierType.cnpj and 
            len(value) != CNPJ_LENGTH):
        raise ValueError('CNPJ must have exactly 14 digits')
        
    return value
```

## Validation Logic

The validation ensures:

1. For CPF type identifiers:
   - The identifier must be exactly 11 digits in length
   - If not, a validation error is raised

2. For CNPJ type identifiers:
   - The identifier must be exactly 14 digits in length
   - If not, a validation error is raised

3. For update operations:
   - The validation only occurs if both `identifier` and `type_identifier` are provided
   - If `identifier` is `None`, no validation is performed
   - If `type_identifier` is `None`, no validation is performed

## Testing

The test suite has been updated to:

1. Use valid identifiers in all test cases:
   - "12345678901234" for CNPJ tests (14 digits)
   - "12345678901" for CPF tests (11 digits)

2. Ensure validation works correctly for both creation and update operations

## Note on Future Improvements

This implementation validates only the length of the identifiers. Future improvements could include:

1. Validation of the numerical format (ensuring only digits are used)
2. Checksum validation to verify that the identifiers follow the official calculation algorithm
3. Formatting options to handle identifiers with or without punctuation

## Related Files

The changes were implemented in:

1. `backend/src/schemas/clients.py` - Added validation logic
2. `backend/tests/conftest.py` - Updated test fixtures
3. `backend/tests/routes/test_clients.py` - Updated test cases 