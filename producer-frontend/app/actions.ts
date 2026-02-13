'use server'
import { cookies } from "next/headers"


export async function getCookies  ()  {
    console.log('get Cookies')
    const session_cookie = (await cookies()).get('session')
    console.log(session_cookie)
    return session_cookie
}

// send datas to fastapi server
export async function updateReadingDatas (readingDate: string, meterReading: string, meterNumber: string) {
  console.log('update ReadingDatas')
    const session_cookie = await getCookies()
    console.log(session_cookie)
    console.log(readingDate)
    console.log(meterReading)
    console.log(meterNumber)
    console.log('vor response')
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/home/add`, {method: 'POST', headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        Cookie: `${session_cookie?.name}=${session_cookie?.value}`,
      }, body: JSON.stringify({"reading_date": readingDate, "reading_meter_number":  meterNumber, "meter_number": meterReading})})
    const result  = await response.json()
    const result_status = response.status
    const result_message = response.statusText
    return [result_status, result, result_message]
}

// get datas from the past
export async function getReadingDatas (): Promise<any>{
    const url = `${process.env.NEXT_PUBLIC_API_URL}/home/get`
    const session_cookie = await getCookies()
    const res = await fetch(url, {headers: {
      Cookie: `${session_cookie?.name}=${session_cookie?.value}`
    }})
    const result = await res.json()
    
    // The backend returns a JSON string containing a list of JSON strings.
    // We need to double parse to get the actual objects.
    let parsedData = result;
    if (typeof result === 'string') {
        try {
            parsedData = JSON.parse(result);
        } catch (e) {
            console.error("Failed to parse outer JSON:", e);
            return [];
        }
    }
    
    if (Array.isArray(parsedData)) {
        return parsedData.map((item: any) => {
            if (typeof item === 'string') {
                try {
                    return JSON.parse(item);
                } catch (e) {
                    console.error("Failed to parse inner JSON:", e);
                    return {};
                }
            }
            return item;
        });
    }
    
    return [];
}

export async function getLastData (): Promise<any>{
  const url = `${process.env.NEXT_PUBLIC_API_URL}/home/getLast`
  const session_cookie = await getCookies()
  const res = await fetch(url, {headers: {
    Cookie: `${session_cookie?.name}=${session_cookie?.value}`
  }})
  const result = await res.json()
  return result
}

export async function getNewDatasFromSensor (): Promise<any>{
  const url = `${process.env.NEXT_PUBLIC_API_URL}/home/new`
  const session_cookie = await getCookies()
  const res = await fetch(url, {headers: {
    Cookie: `${session_cookie?.name}=${session_cookie?.value}`
  }})
  const result = await res.json()
  return result
}


