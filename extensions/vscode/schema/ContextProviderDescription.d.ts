/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Title = string;
export type DisplayTitle = string;
export type Description = string;
export type Dynamic = boolean;
export type RequiresQuery = boolean;

export interface ContextProviderDescription {
  title: Title;
  display_title: DisplayTitle;
  description: Description;
  dynamic: Dynamic;
  requires_query: RequiresQuery;
  [k: string]: unknown;
}
