let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
let USER_ID = $('#logged-in-user').val()
let USER_NAME = $('#logged-in-user_name').val()
let csrftoken = $("input[name=csrfmiddlewaretoken]").val();
let active_thread_id = null
let active_chat_username = null

let loc = window.location
let wsStart = 'ws://'

// console.log(loc + ' v ' + loc.host+ ' v ' + loc.hostname+ ' v ' + loc.protocol);
if(loc.protocol === 'https') {
    wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    // console.log('open', e)
    send_message_form.on('submit', function (e){
        e.preventDefault()
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()

        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': send_to,
            'thread_id': thread_id
        }
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}


function newMessage(message, sent_by_id, thread_id) {
	if ($.trim(message) === '') {
		return false;
	}
	let message_element;
	let chat_id = 'chat_' + thread_id
	if(sent_by_id == USER_ID){
	    message_element = `
			<div class="d-flex mb-4 replied">
				<div class="msg_cotainer_send">
					${message}
					<span class="msg_time_send">8:55 AM, Today</span>
				</div> 
			</div>
	    `
    }
	else{
	    message_element = `
           <div class="d-flex mb-4 received">
              
              <div class="msg_cotainer">
                 ${message}
              <span class="msg_time">8:40 AM, Today</span>
              </div>
           </div>
        `

    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
	message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
	input_message.val(null);
}


$('.contact-li').on('click', function (){
    $(this).addClass('active').siblings().removeClass('active')
 
    // message wrappers
    let chat_id = $(this).attr('chat-id')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id +'"]').addClass('is_active')

    chech_first_msg(get_active_thread_id())
})

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    active_thread_id = thread_id;

    console.log(active_thread_id);
    return thread_id
}

  



// search query handler

let search_query = null 

$(document).on('keyup', '.all-search-box', function(e) {
    search_query = $('.all-search-box').val()

    // AJAX request for search query
    var xhr = new XMLHttpRequest();
    var url = `${loc}search_user`;
   
    xhr.open("POST", url, true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken); 
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) { 
            let response = JSON.parse(xhr.response) 
            $('.search-result').empty()
            response.map( (item, key) => {
                $('.search-result').append(`
                    <div class="single-div d-flex justify-content-between">
                        <div class="d-flex justify-content-between">
                            <div class="res-user-img">
                                <img src="/static/image/userlogo.jpeg" class="rounded-circle" alt="user img">
                            </div>
                            <div class="res-user-name my-auto mx-3">
                                <p class="my-auto">${item.username}</p>
                            </div>
                        </div>
                        <div class="res-actions">
                            <button id="user_id_${item.id}" onclick="say_hi(${USER_ID}, ${item.id}, '${item.username}')" class="btn btn-primary say-hi-btn my-auto px-3 py-0">Say, Hi</button>
                        </div>
                    </div>
                    <hr class="my-2 text-light">
                `);
            });
        }
    };
    xhr.send(`query=${search_query}`);

});


const say_hi = (user_id, receiver_id, param_username) => {
    // AJAX request for saying auto generated "hi"
    var xhr = new XMLHttpRequest();
    var url = `${loc}createnewthread`;
    
    xhr.open("POST", url, true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken); 
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) { 
            let response = JSON.parse(xhr.response)
            console.log(response);
            let chat_id = response[0].id;
 
            let other_user_id = (response[0].first_person_id == USER_ID) ? response[0].second_person_id : response[0].first_person_id;
            
            $('.contacts').append(`
                <li class="active contact-li "  chat-id="chat_${response[0].id}" style="cursor: pointer">
                    <div class="d-flex bd-highlight">
                        <div class="img_cont">
                            <img src="/static/image/userlogo.jpeg" class="rounded-circle user_img"
                                alt="">
                            <!-- <span class="online_icon"></span> -->
                        </div>
                        <div class="user_info">
                            <span>${param_username} </span>
                        </div>
                    </div>
                </li> 
                 
            `);

            $('.card').append(`
                <div class="messages-wrapper hide " chat-id="chat_${response[0].id}" other-user-id="${other_user_id}">
                    <div class="card-header msg_head ">
                        <div class="d-flex bd-highlight header-inner ">
                            <div class="img_cont">
                                <img src="/static/image/userlogo.jpeg" class="rounded-circle user_img">
                                <span class="online_icon"></span>
                            </div>
                            <div class="user_info">
                                <span>${param_username}</span>
                            </div>
                            <div class="video_cam">
                                <!-- <span><i class="fas fa-video"></i></span>
                                <span><i class="fas fa-phone"></i></span> -->
                            </div>
                        </div> 
                    </div>

                    <div class="card-body msg_card_body ">
                            <!------- messages ------->
                        <div class="d-flex mb-4 replied">
                            <div class="msg_cotainer_send">
                                Hi, this is auto generated.
                                <span class="msg_time_send">${response[0].timestamp}</span>
                            </div>
                        </div>
                        <!------- messages ------->
                    </div> 
                </div>
            `);
        
            $('.contact-li').addClass('active').siblings().removeClass('active')
            
            // message wrappers 
            $('.messages-wrapper.is_active').removeClass('is_active')
            $('.messages-wrapper[chat-id="' + chat_id +'"]').addClass('is_active')
        
            chech_first_msg(get_active_thread_id())
            console.log('ho jaa');
        }
    };
    xhr.send(`user_id=${user_id}&receiver_id=${receiver_id}`);
   
}
 

const chech_first_msg = (active_thread_id) => {
    console.log(active_thread_id, 'initial');

    // AJAX request for checking first msg or not
    var xhr = new XMLHttpRequest();
    var url = `${loc}checkfirstmsg`;
    
    xhr.open("POST", url, true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken); 
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) { 
            
            let res = JSON.parse(xhr.response)
            console.log('first_sender :- ', res);

            if(res[0].first_sender_id != USER_ID) {
                if(res[0].is_first_msg == true) {
                    $('.accept-decline-div').removeClass('check-active')
                    $('.typing-msg-div').addClass('check-active')

                    $('#first_sender').text(param_username)
                } 
                else {
                    $('.typing-msg-div').removeClass('check-active')
                    $('.accept-decline-div').addClass('check-active')
                }
            }
            else {
                $('.typing-msg-div').removeClass('check-active')
                $('.accept-decline-div').addClass('check-active')
            }
        }
    };
    xhr.send(`active_thread_id=${active_thread_id}`);
   
}
 
const abc = () => {
    $('.accept-decline-div').removeClass('check-active')
    $('.typing-msg-div').addClass('check-active')
}

const first_msg_status_update = () => {
    console.log(active_thread_id);

    $('.accept-btn').html(`<div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>`);
    
    // AJAX updating the is_first_msg 
    var xhr = new XMLHttpRequest();
    var url = `${loc}updatefirstmsgstatus`;
    
    xhr.open("POST", url, true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken); 
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) { 
           
            
            $('.accept-btn').html(`Yes, Aceept`)

            $('#acc-dic-div').addClass('check-active')
            $('#typing-msg').removeClass('check-active')

            console.log(xhr.response);
            // if(xhr.response == 'status_updated') {
            //     $('.accept-decline-div').removeClass('check-active')
            //     $('.typing-msg-div').addClass('check-active')
            // } 
            // else {
                // console.log(xhr.response);
            // }
        }
    };
    xhr.send(`active_thread_id=${active_thread_id}`);
   
}