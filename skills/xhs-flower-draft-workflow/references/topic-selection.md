# Topic Selection

## Core Rule

Choose topics according to buyer search intent, not generic popularity. The preferred order is:

1. 地域花店词: `#{城市}花店`
2. 地域订花词: `#{城市}订花`
3. 同城成交词: `#{城市}同城鲜花` / `#{城市}鲜花配送`
4. 人群词: `#送女朋友花束` / `#送闺蜜花束` / `#送妈妈花束`
5. 城市场景词: `#{城市}生日花束`
6. 通用场景词: `#纪念日花礼` / `#约会花束`
7. 产品/花材/形态词: `#绣球花篮` / `#蝴蝶兰花篮` / `#粉白花篮`

Use 8-10 topics. Put local buyer-intent terms before broad product style terms.

## Flower Basket Example

For a Chengdu pink-white hydrangea and phalaenopsis basket:

```text
#成都花店 #成都订花 #成都同城鲜花 #成都鲜花配送 #送女朋友花束 #成都生日花束 #纪念日花礼 #绣球花篮 #蝴蝶兰花篮 #粉白花篮
```

## Why This Order

- The first four topics help local buyers find the shop.
- The middle topics match gift intent and occasion.
- The final topics describe the actual product, making the content relevant without becoming generic.

## Topic Binding

When a publishing tool supports platform-direct topic binding:

- Pass only topics confirmed by Xiaohongshu's topic suggestion UI or creator topic API.
- If a topic does not resolve to a real platform topic, omit it from bound topics.
- Do not silently replace failed platform topics with plain hashtag text in the body.
- Report manual topic suggestions to the user when binding fails.
