use std::env;
use tokio;


#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let client = reqwest::Client::new();
    let resp = client.get(env::args().nth(1).unwrap())
        .header("User-Agent", "reqwest")
        .send()
        .await?;

    println!("{resp:#?}");

    Ok(())
}
