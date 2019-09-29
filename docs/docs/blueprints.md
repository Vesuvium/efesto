# Blueprints

Blueprints are convenient way to create types in Efesto.


```yml
# blueprint.yml
version: 2
types:
    pizzas:
        - name
        - price:
            field_type: int
```

When we run `efesto load blueprint.yml`, a pizzas table will be
created. If we start efesto, a `/pizzas` endpoint will be available and will be able to create, read, update and delete pizzas.


## Fields

Blueprints fields default to non-nullable strings:

```yml
types:
    ingredients:
        - name
```

We can specify a field's type:


```yml
types:
    ingredients:
        - name
        - quantity:
            field_type: int
        - last_check:
            field_type: datetime
        - weight:
            field_type: float
```

Supported field types are: `string`, `text`, `int`, `bigint`, `float`, `double`,
`decimal`, `boolean`, `date` and `datetime`.


### Unique fields

We can mark fields as unique:


```yml
types:
    ingredients:
        - name:
            unique: true
```


### Nullable fields

We can mark fields as nullable:

```yml
types:
    ingredients:
        - name
        - last_check:
            field_type: datetime
            nullable: true
```


### Foreign keys

To create foreign keys, we can set a field's `field_type` to the corresponding
type:


```yml
types:
    sizes:
        - name

    pizzas:
        - name
        - price:
            field_type: int
        - size:
            field_type: sizes
```


### Many-to-many

To create a many-to-many relationship, we will to define a foreign keys for
two types:

```yml
types:
    chefs:
        - name

    pizzas:
        - name
        - price:
            field_type: int

    orders:
        - pizza:
            field_type: pizzas
        - chef:
            field_type: chefs
```
