// const host = "http://localhost:8000";
const host = "http://192.168.1.3";
// const host = "http://localhost:8000";
let loggedIn = false;


const loginBtn = document.getElementById("login_button");
const login_check_btn = document.getElementById("login_check");

const loginForm = document.getElementById("login_form");
const username_field = document.getElementById("username_input");
const pass_field = document.getElementById("password_input");

const user_data_box = document.getElementById("loggedInBox");
const user_info = document.getElementById("user_info_span");
const loginBox = document.getElementById("login_box");

const table_buttons = document.querySelectorAll(".table_button");
const table_orders = document.getElementById("table_orders");

const product_table = document.getElementById("product_table_body");
const adding_product_input = document.getElementById("adding_product");

const endTableForm = document.getElementById("end_table_form");
const endTableBox = document.getElementById("end_table_modal");

let current_table = null;

const all_tables = []

function sendLogout(){
    $.post(`${host}/api/user/logout/`,{}, function(data, status){
        // console.log(data);
        location.reload();
    })
}


function checkTables(tb_num=""){
    $.get(`${host}/api/ordering/table/`, function(data, status){
        // console.log(data);

        data.forEach(table => {
            let table_num = table["table_number"];
            // console.log(table_num);
            if (table["orders"]){
                // let activeTable = document.createElement("span");
                // activeTable.id = `active_table_${table_num}`;
                // activeTable.classList.add("active_table_star");
                // activeTable.textContent = "*";
                document.getElementById(`table_${table_num}`).classList.add("active_table");
                // document.getElementById(`table_${table_num}`).append(activeTable);
                // console.log("ADDED A STAR")
            }
        })
    })
}


function checkLogin(){
    $.get(`${host}/api/user/user_info/`, function(data, status){
        if (data["success"]){
            loggedIn = true;
            $.get(`${host}/api/user/user_info/`, function(data, status){
                // console.log(data);
                user_info.textContent = `${data["first_name"]} ${data["last_name"]} (${data["username"]})`;
                checkTables();
            })
            loginBox.style.display = "none";
            user_data_box.style.display = "block";
        }
    })
}

loginForm.addEventListener("submit", function(e){
    e.preventDefault();
    let username = username_field.value;
    let password = pass_field.value;
    $.post(`${host}/api/user/login/`, {username: username, password: password}, function(data, status){
        // console.log(data);
        if (data["success"]){
            // console.log("Logged in");
            loggedIn = true;
            $.get(`${host}/api/user/user_info/`, function(data, staus){
                // console.log(data);
                user_info.textContent = `${data["first_name"]} ${data["last_name"]} (${data["username"]})`;
                checkTables();
            })
            loginBox.style.display = "none";
            user_data_box.style.display = "block";
        }
        else{
            // console.log("Bad credentials");
            alert("Bad credentials");
            username_field.value = "";
            pass_field.value = "";
        }
        // console.log(`${data} and status is ${status}`);
    });

})

function removeOrder(orderId){
    $.ajax({
        url : `${host}/api/ordering/order/`,
        method : 'delete',
        data : {
           order_id: orderId
        },
        success: function(data){
            // console.log(data);
            $(`#order_id_${orderId}`).remove();
            $(`#end_order_id_${orderId}`).remove();
            $("#table_price").text(`${data['table']['price']} $`);
            $("#end_table_price").text(`${data['table']['price']} `);
            if (!data['table']['orders']){
                table_orders.innerHTML = "<h4>No orders yet</h4>";
                $(`#table_${data["table"]["table_number"]}`).removeClass("active_table");
            }
        }
   })
   
   checkTables(tb_num=current_table);
}

table_buttons.forEach(table => {
    table.addEventListener('click', function(e) {
        // console.log("Clicked on a table");
        let table_number = this.id.split("_")[1];
        current_table = table_number;
        // console.log(table_number);
        let animation = "heartBeat";
        product_table.innerHTML = "";
        adding_product_input.value = "";
        $("#table_information").css("display", "block");
        $(`#table_${table_number}`).addClass(`animate__animated animate__delay-0s animate__${animation}`);
        $.get(`${host}/api/ordering/table/${table_number}`, function(data, status){
            // console.log(data);
            // data = data[0];
            $("#table_number").text(data['table_number']);
            $("#table_price").text(`${data['price']} $`);
            table_orders.innerHTML = "";
            if (data["orders"]){
                let all_orders = data["orders"];
                all_orders.forEach(order => {
                    let newLi = document.createElement('li');
                    newLi.id = `order_id_${order['id']}`;
                    newLi.innerHTML = `${order['product_name']}, ${order["price"]} <button onclick="removeOrder(${order['id']})">Delete</button>`;
                    table_orders.append(newLi);
                });
            } else {
                if (!data["orders"]){
                    table_orders.innerHTML = "<h4>No orders yet</h4>";
                }
            }
            
        })
        setTimeout(function(e){
            $(`#table_${table_number}`).removeClass(`animate__animated animate__delay-0s animate__${animation}`);
        }, 1000)
    });
  });


function addOrder(table_num, productId){
    
    $.post(`${host}/api/ordering/order/`, {table_number: table_num, product_id: productId}, function(data, status){
        // console.log(data);
        $("#table_price").text(`${data['table']['price']} $`);
        table_orders.innerHTML = "";
        data['table']['orders'].forEach(order => {
            let newLi = document.createElement('li');
            newLi.id = `order_id_${order['id']}`;
            newLi.innerHTML = `${order['product_name']}, ${order["price"]}, <button onclick="removeOrder(${order['id']})">Delete</button>`;
            table_orders.append(newLi);
        });
    });
    $(`#table_${table_num}`).addClass("active_table");


}

adding_product_input.addEventListener("keyup", function(e){
    let name = this.value
    $.get(`${host}/api/ordering/product/?name=${name}`, function(data, staus){
        // console.log(data);
        product_table.innerHTML = "";
        data.forEach(product => {
            let newTr = document.createElement('tr');
            newTr.innerHTML = `
                <td><img class="product_image" src="${host}${product["image"]}" alt=""></td>
                <td>${product["name"]}</td>
                <td>${product["price"]}</td>
                <td><button onclick="addOrder(${current_table}, ${product['id']})">Add</button></td>
            `;
            product_table.append(newTr);
        })
        
    })
})

function openBox(){
    endTableBox.style.display = "block";
    $("#page_content").addClass("modal_active");
    $.get(`${host}/api/ordering/table/${current_table}`, function(data, staus){
        // console.log(data);
        $("#end_table_number").text(data['table_number']);
        $("#end_table_price").text(`${data['price']} `);
        $("#end_table_button").val(data['table_number']);
        $("#end_table_given").val(data['price']);
        $("#end_table_given").attr({"min": data['price']});
        let end_table_orders = document.getElementById("end_table_orders");
        end_table_orders.innerHTML = "";
        if (data["orders"]){
            let all_orders = data["orders"];
            all_orders.forEach(order => {
                let newLi = document.createElement('li');
                newLi.id = `end_order_id_${order['id']}`;
                newLi.innerHTML = `${order['product_name']}, ${order["price"]}, <button onclick="removeOrder(${order['id']})">Delete</button>`;
                end_table_orders.append(newLi);
            });
        } else {
            if (!data["orders"]){
                end_table_orders.innerHTML = "<h4>No orders yet</h4>";
            }
        }
        
    })

}

function closeBox(){
    endTableBox.style.display = "none";
    $("#page_content").removeClass("modal_active");
}

endTableForm.addEventListener("submit", function(e){
    e.preventDefault();
    $.post(`${host}/api/ordering/end/`, {table_number: $("#end_table_button").val(), paid_with: $("#end_table_given").val()}, function(data, status){
        closeBox();
        $("#table_information").css("display", "none");
        $('#today_info').css('display', 'none');
        $(".loader").css("display", "block");
        alert(`Table has been completed, tip is: ${data["tip_amount"]}`);
        $(`#table_${current_table}`).removeClass("active_table");
        setTimeout(todayInfo, 500);
    })
})


function todayInfo(){
    
    $(".loader").css("display", "block");
    $('#today_info').css('display', 'none');
    $.get(`${host}/api/ordering/today_info/`, function(data, status){
        // console.log(data);
        
        $(".loader").css("display", "none");
        $("#total_revenue").text(data["total_revenue"]);
        $("#total_tips").text(data["tip_amount"]);
        $("#total_tables").text(data["total_tables"]);
        $('#today_info').css('display', 'block');
        
    })
    
}





document.onload = checkLogin();