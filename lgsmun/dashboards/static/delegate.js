var button_lock=false;
var zoom_link='';
var drive_link='';
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
function raise_motion(){
  $.post("raise_motion",{
    'motion':$('#motion').val(),
    'csrfmiddlewaretoken':csrftoken
  });

}
function sendmessage(){
  $.post("send_message",{
    'message':$('#message').val(),
    'recipient':$('#recipient').val(),
    'csrfmiddlewaretoken':csrftoken
  });
  $('#message').val('');
}
function raise_point(){
  if(!button_lock){
  $.post("send_notification",{
    'notification':'(POINT)'+$('#point').val(),
    'csrfmiddlewaretoken':csrftoken
  });
  button_lock=true;
  setTimeout(unlock,30000);
}}
function unlock(){
  button_lock=false;
  clearTimeout(unlock);
}
var duration=0;
var counter=0;
var total_time=0;
var total_count=0;
var status='';
function timer(){

$('#minutes').html(Math.trunc(counter/60).toLocaleString(undefined, {minimumIntegerDigits: 2}));
    $('#seconds').html((counter%60).toLocaleString(undefined, {minimumIntegerDigits: 2}));
    $('#total_minutes').html(Math.trunc(total_count/60).toLocaleString(undefined, {minimumIntegerDigits: 2}));
    $('#total_seconds').html((total_count%60).toLocaleString(undefined, {minimumIntegerDigits: 2}));

  if((status!='pause')&&(status!='stop')){


    if (counter!=0){
    counter=counter-1;
    if ((total_count!=0 && status=='start')){

      total_count=total_count-1;

    }
}
}
}
var prevchat='';
var ws= new WebSocket("ws://"+window.location.host+'/ws/delegate/');
var ess_data={'committee':$('#committee_name').html(),'country':$('#country').val(),'uuid':$('#uuid').val(), 'iteration':-1, 'total_time':total_count, 'speaker_time':counter};
ws.onopen=function(){
  ess_data={'committee':$('#committee_name').html(),'country':$('#country').val(),'uuid':$('#uuid').val(), 'iteration':-1, 'total_time':total_count, 'speaker_time':counter};
  console.log(ess_data);
ws.send(JSON.stringify(ess_data));
};
ws.onmessage=async function(event){
if(event.data!="NULL"){
  var data=JSON.parse(event.data);
  console.log(data);
  $('#att').html(data.countrylist);
  $('#current_mod').html(data.current_mod);
  $('#current_topic').html(data.current_topic);
  $('#speaking_mode').html(data.speaking_mode);
  $('#notifications').html(data.notifications);
  $('#gsl').html(data.gsl);
  $('#rsl').html(data.rsl);
  $('#inbox').html(data.inbox);
  if((data.inbox!=prevchat)&&(current_state!='chat')){
    $('#Chat').html("Chat <span class='whitedot'></span>");
  }
  prevchat=data.inbox;
  updateScroll();
  $('#mod_table').html(data.mods);
  ess_data['iteration']=data.iteration;
  ess_data['total_time']=total_count;
  ess_data['speaker_time']=counter;
  zoom_link=data.zoom_link;
  drive_link=data.drive_link;
  status=data.timer_status;
  if(parseInt(data.total_time)!=total_time){
    total_time=parseInt(data.total_time);
    total_count=total_time;
  }
  if ('start'==data.timer_status && duration!=parseInt(data.timer_duration)){
    status=data.timer_status;
      duration=parseInt(data.timer_duration);
      counter=duration;
  }
  else if(data.timer_status=='stop'){
    status=data.timer_status;
    duration=0;
    counter=0;
  }}
  await sleep(1000);
  ws.send(JSON.stringify(ess_data));
  console.log(ess_data);
  console.log('sent');
};
setInterval(function(){ess_data['total_time']=total_count;
  ess_data['speaker_time']=counter;ws.send(JSON.stringify(ess_data));},1000);
setInterval(timer,1000);
function updateScroll(){
    $('#inbox').scrollTop($('#inbox')[0].scrollHeight);
    clearInterval(updateScroll);
}
function remove_chat_dot(){
$('#Chat').html("Chat");
$('#inbox').html(prevchat);
}
var current_state='';
