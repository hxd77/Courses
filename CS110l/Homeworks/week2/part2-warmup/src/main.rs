use std::io;
use std::io::Write;

fn promt_user_input(promt:&str)->String{
    print!("{}",promt); //print不会在后面加换行符
    io::stdout().flush().unwrap(); //print!不会自动刷新缓冲区，所以要用flush
    let mut input=String::new();
    io::stdin().read_line(&mut input);
    input.trim().to_string() //trim()去掉字符串末尾的空白字符(\n),返回一个&str,to_string()再把它转会String类型返回
}

fn read_shopping_list()->Vec<String>{
    let mut shopping_list:Vec<String>=Vec::new();
    loop{
        let input =promt_user_input("Enter an item to add to the list: ");
        if input.to_lowercase().trim() == "done"{
            break;
        }
        shopping_list.push(input);
    }
    shopping_list
}

fn print_shopping_list(shopping_list:&Vec<String>){
    println!("Remember to buy");
    for item in shopping_list{
        println!("* {}",item);
    }
}

fn main(){
    let shopping_list = read_shopping_list();
    print_shopping_list(&shopping_list);
}