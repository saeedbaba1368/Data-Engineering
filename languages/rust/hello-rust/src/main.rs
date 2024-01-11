use ferris_says::say; // from the previous step
use std::io::{stdout, BufWriter};
use std::collections;

fn main() {
    let stdout = stdout();
    let message = String::from("Hello fellow Rustaceans!");
    let width = message.chars().count();

    let mut writer = BufWriter::new(stdout.lock());
    say(message.as_bytes(), width, &mut writer).unwrap();

    let my_tuple = (10, "Hello, World!", false);
    let (x, y, z) = my_tuple;
    
    println!("The first element is: {}", x);
    println!("The second element is: {}", y);
    println!("The third element is: {}", z);

    let mut my_array = [1, 2, 3, 4, 5];

    // Accessing elements
    println!("The first element is: {}", my_array[0]);
    
    // Modifying elements
    my_array[0] = 100;
    println!("The first element after modification is: {}", my_array[0]);
    
    // Looping over an array and manipulating elements
    for i in 0..my_array.len() {
        my_array[i] *= 2;
    }
    
    // printing the array
    println!("The array after manipulation: {:?}", my_array);
}