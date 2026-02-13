import { SVGProps } from "react";

export type IconSvgProps = SVGProps<SVGSVGElement> & {
  size?: number;
};

export interface ISmartlandSMGW  {
  id: string;
  user_id: string;
  ts: Date;
  meter_id: number;
  receive_ts: Date
  value: number;
  unit: string;
  obis: string;
}
export interface ISmartlandSMGWRow  {
  key: number;
  id: string;
  user_id: string;
  ts: Date;
  meter_id: number;
  receive_ts: Date
  value: number;
  unit: string;
  obis: string;
}
