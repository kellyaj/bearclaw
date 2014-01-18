Trello.authorize({
  name: "Bearclaw",
  scope: {read: true},
  expiration: "never"
});

var cardTrapper = new CardTrapper(Trello);
cardTrapper.getCards();
