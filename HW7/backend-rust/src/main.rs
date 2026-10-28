fn main() {
    println!("Rust 伺服器啟動中...");
}

// 核心商業邏輯 (被測試的目標)
fn calculate_discount(price: f64, discount_rate: f64) -> f64 {
    price * (1.0 - discount_rate)
}

// 1. 單元測試 (Unit Tests)
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_discount() {
        let original_price = 100.0;
        let discount = 0.2;
        assert_eq!(calculate_discount(original_price, discount), 80.0);
    }
    
    #[test]
    fn test_no_discount() {
        assert_eq!(calculate_discount(50.0, 0.0), 50.0);
    }
}
