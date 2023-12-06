/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type Filepath = string;
export type Lineno = number;
export type Function = string;
export type Code = string | null;
export type Frames = TracebackFrame[];
export type Message = string;
export type ErrorType = string;
export type FullTraceback = string | null;

export interface Traceback {
  frames: Frames;
  message: Message;
  error_type: ErrorType;
  full_traceback?: FullTraceback;
  [k: string]: unknown;
}
export interface TracebackFrame {
  filepath: Filepath;
  lineno: Lineno;
  function: Function;
  code?: Code;
  [k: string]: unknown;
}
