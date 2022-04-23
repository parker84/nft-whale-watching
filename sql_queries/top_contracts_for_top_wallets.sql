WITH 

top_wallets as (
    select *
    from `bigquery-public-data.crypto_ethereum.balances`
    order by eth_balance desc
    limit 1000
)

SELECT 
    contracts.address as contract_address, 
    COUNT(1) AS transaction_count,
FROM `bigquery-public-data.crypto_ethereum.contracts` AS contracts
JOIN `bigquery-public-data.crypto_ethereum.transactions` AS transactions ON (transactions.to_address = contracts.address)
JOIN top_wallets as tw ON (tw.address = transactions.from_address)
WHERE contracts.is_erc721 = TRUE
GROUP BY contracts.address
ORDER BY transaction_count DESC
LIMIT 10
