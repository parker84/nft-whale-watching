WITH 

top_wallets as (
    select *
    from `bigquery-public-data.crypto_ethereum.balances`
    order by eth_balance desc
    limit 1000
)

SELECT 
    tokens.address as token_address, 
    tokens.name as token_name,
    COUNT(1) AS transfer_count,
FROM `bigquery-public-data.crypto_ethereum.tokens` AS tokens
JOIN `bigquery-public-data.crypto_ethereum.token_transfers` AS transactions ON (transactions.to_address = tokens.address)
JOIN top_wallets as tw ON (tw.address = transactions.from_address)
GROUP BY 1,2
ORDER BY 3 DESC
LIMIT 10
