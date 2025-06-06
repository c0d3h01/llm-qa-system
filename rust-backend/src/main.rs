use actix_web::{web, App, HttpServer, Responder, HttpResponse};
use serde::{Deserialize, Serialize};
use reqwest::Client;

#[derive(Deserialize, Serialize)]
struct QueryPayload {
    question: String,
}

#[derive(Serialize, Deserialize)]
struct QueryResponse {
    answer: String,
    sources: Vec<String>,
}

async fn api_status() -> impl Responder {
    HttpResponse::Ok().body("LLM-QA Backend is running")
}

async fn api_query(
    payload: web::Json<QueryPayload>,
    data: web::Data<AppState>
) -> impl Responder {
    let client = &data.http;
    let ml_url = format!("{}/inference", data.ml_inference_url);
let ml_resp: QueryResponse = match client.post(&ml_url)
    .json(&*payload)
    .send().await
{
    Ok(resp) => match resp.json::<QueryResponse>().await {
        Ok(val) => val,
        Err(_) => QueryResponse {
            answer: "ML inference failed".into(),
            sources: vec![],
        }
    },
    Err(_) => QueryResponse {
        answer: "ML inference failed".into(),
        sources: vec![],
    }
};    HttpResponse::Ok().json(ml_resp)
}

struct AppState {
    http: Client,
    ml_inference_url: String,
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();
    let ml_inference_url = std::env::var("ML_INFERENCE_URL").unwrap_or("http://localhost:8000".to_string());
    let state = web::Data::new(AppState{
        http: Client::new(),
        ml_inference_url,
    });
    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .route("/api/status", web::get().to(api_status))
            .route("/api/query", web::post().to(api_query))
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}