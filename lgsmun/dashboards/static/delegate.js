function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
var ws= new WebSocket("ws://"+window.location.host+'/ws/delegate/');
ws.onopen=function(){
ws.send($('#committee_name').html());
};
ws.onmessage=async function(event){
  var data=JSON.parse(event.data);
  console.log(data);
  $('#att').html(data.countrylist);
  $('#current_mod').html(data.current_mod);
  $('#current_topic').html(data.current_topic);
  $('#speaking_mode').html(data.speaking_mode);
  $('#notifications').html(data.notifications);
  $('#gsl').html(data.gsl);
  $('#rsl').html(data.rsl);
  await sleep(1000);
  ws.send($('#committee_name').html());
};
