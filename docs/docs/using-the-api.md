# Using the API

Efesto has a uniform CRUD API. By default only `/users`, `/types` and `/fields`
are available.

You can create more endpoints with a blueprint.


## Authentication

In order to authenticate, you need to send a JWT bearer token in the
authorization header corresponding to the user. See configuration for how to
generate the token.

## Permissions

Efesto implements UNIX-style permissions. Every item has an owner and a group
and different levels of permissions for its owner, group and anyone else.

Efesto uses numbers from 0 to 3, instead of 0 to 7:

- 0: no permission
- 1: read
- 2: edit
- 3: delete

When an item is created, the user sending the request will be the owner and the
user's group will be the group of the item.

Default permissions for new items are set to 300, equivalent to a UNIX 700.

## Collections

Collections endpoint support POST and GET requests.

## GET

Get supports a number of parameters to filter, sort and embed items:

- `_embeds`: embeds types that have foreign keys to the requested type. Use commas to separate more types.
- `_order`: the field and direction for items' order. For example `_order=-id` or `_order=owner_id`
- `page` and `items` for paginations.
- filters on fields, for example: `field=value`. Supports `field=!value`, `field=>value`, `field=<value`, `field=~va`, `field=[1, 2]`


## Items

Supports GET, PATCH and DELETE requests.
