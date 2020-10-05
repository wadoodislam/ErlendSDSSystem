
### Manufacturer:
    **name:** CharField for manufacturer's name, and can have maximum length of 20 characters
    **created_date:** DateTimeField for the creation of manufacturer, and cannot be modified
 
### Language:
    **name:** CharField for language name, and can have maximum length of 30 characters

### Product:
    **name:** CharField for product name, and can have maximum length of 30 characters    
    **language:** ForeignKey field has a many to one relationship with **Language** table and on deletion of language it will also be deleted
    **manufacturer:** ForeignKey and has a many to one relationship with **Manufacturer** table and on deletion of manufacturer it will also be deleted
    **created_date:** DateTimeField for the creation of product, and cannot be modified

### ProducerOfSDS: 
    **name:** CharField for manufacturer's name, and can have maximum length of 20 characters
    **created_date:** DateTimeField for the creation of manufacturer, and cannot be modified

### User:(only have overridden fields)
    **email:** EmailField for user's email and it should be unique
    **phone_number:** PhoneNumberField imported from phonenumber_field.modelfields to store user's phone number
    **hourly_rate_usd:** IntegerField to store hourly rate in usd and can be null
    **url_to_contract:** URLField to store url of the contract and can be null
    
    