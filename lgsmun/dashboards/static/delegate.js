function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
var duration=0;
var counter=0;
var status='';
function timer(){

  if(status!='pause'){

    $('#minutes').html(Math.trunc(counter/60).toLocaleString(undefined, {minimumIntegerDigits: 2}));
    $('#seconds').html((counter%60).toLocaleString(undefined, {minimumIntegerDigits: 2}));
    if (counter!=0){
    counter=counter-1;
}
}
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
  status=data.timer_status
  if ('start'==data.timer_status && duration!=parseInt(data.timer_duration)){
    status=data.timer_status;
      duration=parseInt(data.timer_duration);
      counter=duration;
  }
  else if(data.timer_status=='stop'){
    status=data.timer_status;
    duration=0;
    counter=0;
  }
  await sleep(1000);
  ws.send($('#committee_name').html());
};
setInterval(timer,1000);
