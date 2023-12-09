/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Filepath = string;
export type Line = number;
export type Character = number;
export type Replacement = string;

export interface FileEdit {
  filepath: Filepath;
  range: Range;
  replacement: Replacement;
  [k: string]: unknown;
}
/**
 * A range in a file. 0-indexed.
 */
export interface Range {
  start: Position;
  end: Position;
  [k: string]: unknown;
}
export interface Position {
  line: Line;
  character: Character;
  [k: string]: unknown;
}
