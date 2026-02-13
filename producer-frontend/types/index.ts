import { SVGProps } from "react";

export type IconSvgProps = SVGProps<SVGSVGElement> & {
  size?: number;
};

export interface ISmartlandConsumer  {
  id: string;
  user_id: string;
  reading_date: Date;
  meter_number: number;
  reading_meter_number: number;
  upload_date: Date;
}
export interface ISmartlandConsumerRow  {
  key: number;
  id: string;
  user_id: string;
  reading_date: Date;
  meter_number: number;
  reading_meter_number: number;
  upload_date: Date;
}
