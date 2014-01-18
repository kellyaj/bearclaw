describe("cardTrapper", function() {

  it('creates an card with a name, carrier, and tracking number', function() {
    var rawCard = {
      "name": "some item name",
      "desc": "UPS-SOMETRACKINGNUMBER"
    };
    var expectedCard = {
      name: "some item name",
      carrier: "UPS",
      tracking: "SOMETRACKINGNUMBER"
    };
    var cardTrapper = new CardTrapper();
    cardTrapper.mountCards([rawCard]);
    expect(cardTrapper.cards[0]).toEqual(expectedCard);
  })

});
