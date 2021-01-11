function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
var ws= new WebSocket("ws://"+window.location.host+'/ws/delegate/');
ws.onopen=function(){
ws.send($('#committee_name').html());
};
ws.onmessage=async function(event){
  var data=JSON.parse(event.data);
  $('#att').html(data.countrylist);
  $('#current_mod').html(data.current_mod);
  $('#current_topic').html(data.current_topic);
  $('#speaking_mode').html(data.speaking_mode);
  await sleep(1000);
  ws.send($('#committee_name').html());
};
