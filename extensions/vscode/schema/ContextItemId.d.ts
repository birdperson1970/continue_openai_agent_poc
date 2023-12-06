/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type ProviderTitle = string;
export type ItemId = string;

/**
 * A ContextItemId is a unique identifier for a ContextItem.
 */
export interface ContextItemId {
  provider_title: ProviderTitle;
  item_id: ItemId;
  [k: string]: unknown;
}
