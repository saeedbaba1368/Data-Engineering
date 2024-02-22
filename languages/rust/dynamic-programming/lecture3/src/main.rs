//use std::io;
use rand::Rng;
use std::env;

fn print_message(x: String) {
    println!("The value of x is: {x}");
}

fn sum(n: i32){
    //f(n) = f(n-1) + n
    //calculate sum using recurrence relation
    let n_usize = n as usize;
    let mut arr = vec![0; n_usize-1]; // +1 to include f(0)
    //let mut arr: Vec<i32> = (1..=n).collect();
    arr.insert(0, 0);

    for i in 1..n_usize {
        arr[i] = arr[i - 1] + i as i32;
    }
    if let Some(last_element) = arr.last() {
        println!("Last element, AKA the sum: {}", last_element);
    } else {
        println!("Vector is empty!");
    }

}

fn main() {
    println!("Guess the number beteen 1 and 100!");

    println!("Please input your guess.");
    let mut rng = rand::thread_rng();
    let num_int = rng.gen_range(0..100);
    let num = num_int.to_string();
    //let mut guess = String::new();
    //io::stdin().read_line(&mut guess).expect("Failed to read line");

    let args: Vec<String> = env::args().collect();

    let guess = &args[1];

    println!("You guessed: {}", guess);
    if num == guess.as_str() {
        println!("You guessed correctly!");
    } else {
        println!("Wrong sucker");
        print_message(num);
    }
    let parsed_int: Result<i32, _> = guess.trim().parse();
    // Unwrap the Result to get the i32 value and pass it to sum()
    println!("Its ok, now were gonna calculate the sum");
    match parsed_int {
        Ok(num) => sum(num),
        Err(err) => println!("Failed to parse string to integer: {:?}", err),
    }
}