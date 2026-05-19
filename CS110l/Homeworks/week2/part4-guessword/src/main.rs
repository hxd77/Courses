use std::io;
use std::io::Write;
use rand::RngExt;

const NUM_GUESSES:i32=5;
const WORDS:&[&str]=&[
    "lobster", "crayfish", "elephant", "giraffe", "penguin",
    "dolphin", "butterfly", "mushroom", "keyboard", "lantern",
    "blanket", "captain", "diamond", "fortress", "harvest",
    "journey", "mystery", "oranges", "popcorn", "rustlang",
    "sandcastle", "telescope", "umbrella", "volcano", "whistle",
];

//从单词列表随机选一个单词
fn pick_secret_word()->&'static str{
    let mut rng=rand::rng();
    let index=rng.random_range(0..WORDS.len());
    WORDS[index]
}

//提示用户输入一个字符，返回该字符
fn prompt_user_input(promt:&str)->char{
    print!("{} > ", promt);
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    input.trim().chars().next().unwrap_or(' ')
    //trim()去掉字符串首尾的空白字符(空格、\n)等，返回一个&str
    //.chars()把字符串转换成一个字符迭代器，遍历每一个字符
    //.next()从迭代器中取出第一个元素返回Option<char>
    //.unwrap_or(' ')如果是Some('r')就取出，如果是None,就用' '作为默认值
}

//根据已猜字母，生成当前单词的显示模式(未猜到的用 - 代替)
fn word_so_far(secret:&str,guessd:&Vec<char>)->String{
    secret.
        chars()
        .map(|c| if guessd.contains(&c) {
          c
        }else{'-'})
        .collect()
}

fn main() {
    let secret_word=pick_secret_word();
    let mut guesses_left=NUM_GUESSES;
    let mut guessed_letters:Vec<char>=Vec::new();

    println!("Welcome to Guess the Word!");

    loop{
        let display=word_so_far(&secret_word,&guessed_letters);

        //检查是否已猜出全部字母
        if !display.contains("-"){
            println!(
                "\nCongratulations you guessed the secret word: {}",
                secret_word
            );
            break;
        }

        //检查是否用完了猜测次数
        if guesses_left ==0{
            println!("\nSorry, you ran out of guesses!");
            println!("The word was: {}", secret_word);
            break;
        }
        println!("The word so far is: {}", display);

        //显示已猜过的单词
        let guessed_str:String=guessed_letters.iter().collect();
        println!("You have guessed the following letters: {}", guessed_str);

        println!("You have {} guesses left", guesses_left);

        let guess=prompt_user_input("Please guess a letter: ");
        println!();

        guessed_letters.push(guess);

        //如果猜错了，则减少次数
        if !secret_word.contains(guess){
            println!("Sorry, that letter is not in the word!");
            guesses_left -=1;
        }
    }
}