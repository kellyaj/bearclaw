var CardTrapper = function(service) {
  this.service = service;
  this.boardKey = "52d9a671bd93976f645ea691/cards"
  this.rawCards = []
  this.cards = []
}

CardTrapper.prototype.getCards = function() {
  var self = this;
  this.service.boards.get(this.boardKey, function(rawCards) {
    self.rawCards = rawCards;
    console.log(self.rawCards);
  })
}

CardTrapper.prototype.mountCards = function() {
  var self = this;
  _.each(self.rawCards, function(rawCard) {
    splitDesc = rawCard.desc.split('-')
    var card = {
      name: rawCard.name,
      carrier: splitDesc[0],
      tracking: splitDesc[1]
    };
    self.cards.push(card);
  });
}
