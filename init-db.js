db = db.getSiblingDB("dummy_db")
db.user_tb.drop()

db.user_tb.insertMany ([
    {
        "name": "Pranav",
        "text": "null"
    },
    {
        "name": "Meet",
        "text": "null"
    }
]);

