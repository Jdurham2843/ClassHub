function shuffle(data) {
    for(var i = 0; i < data.length; i++){
      var randNum = Math.floor(Math.random() * (data.length - 0) + 0);
      var temp = data[i];
      data[i] = data[randNum];
      data[randNum] = temp;
    }
  }
    shuffle(data);
    console.log('hello');
    var count = 0;
    var side = 'frontside';
    $('#card').html(data[count]['fields'][side]);

    $('#next').click(function (){
      side = 'frontside';
      if (count < data.length - 1){
        count++;
        $('#card').html(data[count]['fields'][side]);
      } else {
        alert('End of Deck');
      }
    });

    $('#flip').click(function (){
        if (side == 'frontside'){
          side = 'backside';
          $('#card').html(data[count]['fields'][side]);
        } else {
          side = 'frontside';
          $('#card').html(data[count]['fields'][side]);
        }
    });

    $('#reshuffle').click(function(){
      shuffle(data);
      count = 0;
      side = 'frontside';
      $('#card').html(data[count]['fields'][side]);
    })
