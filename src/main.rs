use nom::{
    bytes::complete::tag,
    character::complete::{alpha1, char, newline},
    combinator::map,
    multi::{many1, separated_list1},
    sequence::{delimited, pair, terminated},
    IResult,
};
use std::{collections::HashMap, fs};

fn parse_array(i: &str) -> IResult<&str, Vec<String>> {
    delimited(
        char('['),
        separated_list1(
            tag(", "),
            delimited(
                char('\''),
                map(alpha1, |c: &str| String::from(c)),
                char('\''),
            ),
        ),
        char(']'),
    )(i)
}

fn parse_file(i: &str) -> Vec<(String, Vec<String>)> {
    many1(terminated(
        pair(
            terminated(map(alpha1, |s| String::from(s)), char(' ')),
            parse_array,
        ),
        tag("\r\n"),
    ))(i)
    .unwrap()
    .1
}

fn letter_to_number(c: u8) -> u32 {
    2_u32.pow(c as u32 - 'a' as u32)
}

fn word_to_number(word: String) -> u32 {
    let mut out: u32 = 0;

    for c in word.as_bytes() {
        out += letter_to_number(*c);
    }

    out
}

fn letters_available(letters: u32, word: u32) -> bool {
    letters & word == word
}

fn number_to_letters(mut n: u32) -> String {
    let mut out = String::new();
    let mut i = 0;
    while i < 32 {
        if n & 1 == 1 {
            out.push(('a' as u32 + i) as u8 as char)
        }

        i += 1;
        n = n >> 1;
    }

    out
}

fn main() {
    let file = "lenfive.txt";
    let contents = fs::read_to_string(file).unwrap();
    let parsed = parse_file(contents.as_str());
    let mut words: Vec<String> = Vec::new();
    let mut sequence_to_wordset: HashMap<String, Vec<String>> = HashMap::new();
    for (w, wordset) in parsed {
        words.push(w.clone());
        sequence_to_wordset.insert(w, wordset);
    }

    let mut binary_words: Vec<u32> = Vec::new();
    for word in words {
        binary_words.push(word_to_number(word))
    }

    fn solve_dynamic(
        start: u32,
        alphabet: u32,
        binary_words: &Vec<u32>,
        memo: &mut HashMap<u32, Vec<Vec<u32>>>,
    ) -> Vec<Vec<u32>> {
        match memo.get(&alphabet) {
            Some(ws) => {
                return ws.clone();
            }
            None => {}
        };

        if alphabet.count_ones() == 6 {
            let mut out: Vec<Vec<u32>> = vec![];
            let mut i = start as usize;
            while i < binary_words.len() {
                if letters_available(alphabet, binary_words[i]) {
                    out.push(vec![binary_words[i]])
                }

                i += 1;
            }
            memo.insert(alphabet, out);
            return memo.get(&alphabet).unwrap().clone();
        }

        let mut out: Vec<Vec<u32>> = vec![];
        let mut i = start as usize;
        while i < binary_words.len() {
            let binary_word = binary_words[i];
            if letters_available(alphabet, binary_word) {
                let new_alphabet = alphabet - binary_word;
                let mut sub = solve_dynamic(i as u32 + 1, new_alphabet, binary_words, memo);
                for s in sub.iter_mut() {
                    s.push(binary_word);
                }
                out.append(&mut sub);
            }
            i += 1;
        }

        memo.insert(alphabet, out.clone());
        out
    }

    let alphabet = word_to_number(String::from("abcdefghijklmnopqrstuvwxyz"));

    let mut memo = HashMap::new();
    let begin = std::time::SystemTime::now();
    let solutions = solve_dynamic(0, alphabet, &binary_words, &mut memo);

    let mut count = 0;
    for s in solutions {
        assert_eq!(s.len(), 5);
        let s0 = sequence_to_wordset.get(&number_to_letters(s[0])).unwrap();
        let s1 = sequence_to_wordset.get(&number_to_letters(s[1])).unwrap();
        let s2 = sequence_to_wordset.get(&number_to_letters(s[2])).unwrap();
        let s3 = sequence_to_wordset.get(&number_to_letters(s[3])).unwrap();
        let s4 = sequence_to_wordset.get(&number_to_letters(s[4])).unwrap();

        for w0 in s0 {
            for w1 in s1 {
                for w2 in s2 {
                    for w3 in s3 {
                        for w4 in s4 {
                            println!("{} {} {} {} {}", w0, w1, w2, w3, w4);
                            count += 1;
                        }
                    }
                }
            }
        }
    }
    println!("{} solutions", count);
    let end = std::time::SystemTime::now().duration_since(begin).unwrap();
    println!("in {}ms", end.as_millis());
}
