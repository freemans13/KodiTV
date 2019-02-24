import json

my_dict = {
    'date': '2019-02-21',
    'event': {"bla":1},
    'item': {"foo":2}
}

print(my_dict)

print(json.dumps(my_dict))


print(json.dumps({}))
print(json.loads('{}'))

json_text = '{"date": "2019-02-21", "event": {"bla": 1}, "item": {"foo": 2}}'


my_new_dict = json.loads(json_text)
print(my_new_dict['date'], my_new_dict['event']['bla'])