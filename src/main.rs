use teloxide::prelude::*;

pub type Error = Box<dyn std::error::Error + Send + Sync>;

#[tokio::main]
async fn main() -> Result<(), Error> {
    pretty_env_logger::init();
    log::info!("Starting bot...");
    let bot = Bot::from_env();
    let handler = dptree::entry()
        .branch(Update::filter_message().endpoint(message_handler))
    Dispatcher::builder(bot, handler).enable_ctrlc_handler().build().dispatch().await;
    Ok(())
}
