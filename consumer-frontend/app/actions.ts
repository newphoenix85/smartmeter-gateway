'use server'
import { cookies } from "next/headers"


export async function getCookies() {
  console.log('get Cookies')
  const session_cookie = (await cookies()).get('session')
  console.log(session_cookie)
  return session_cookie
}

// send datas to fastapi server
export async function updateReadingDatas(readingDate: string, meterReading: string, meterNumber: string) {
  const session_cookie = await getCookies()
  const baseUrl = process.env.BACKEND_INTERNAL_URL || process.env.NEXT_PUBLIC_API_URL
  const response = await fetch(`${baseUrl}/home/new`, {
    method: 'POST', headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      Cookie: `${session_cookie?.name}=${session_cookie?.value}`,
    }, body: JSON.stringify({ "reading_date": readingDate, "reading_meter_number": meterReading, "meter_number": meterNumber })
  })
  const result = await response.json()
  const result_status = response.status
  const result_message = response.statusText
  return [result_status, result, result_message]
}

// get datas from the past
export async function getReadingDatas(): Promise<any> {
  const baseUrl = process.env.BACKEND_INTERNAL_URL || process.env.NEXT_PUBLIC_API_URL
  const url = `${baseUrl}/home/get`
  const session_cookie = await getCookies()
  const res = await fetch(url, {
    headers: {
      Cookie: `${session_cookie?.name}=${session_cookie?.value}`
    }
  })
  const result = await res.json()
  return result
}

export async function getLastData(): Promise<any> {
  const baseUrl = process.env.BACKEND_INTERNAL_URL || process.env.NEXT_PUBLIC_API_URL
  const url = `${baseUrl}/home/getLast`
  const session_cookie = await getCookies()
  const res = await fetch(url, {
    headers: {
      Cookie: `${session_cookie?.name}=${session_cookie?.value}`
    }
  })
  const result = await res.json()
  return result
}

export async function getNewDatasFromSensor(): Promise<any> {
  const baseUrl = process.env.BACKEND_INTERNAL_URL || process.env.NEXT_PUBLIC_API_URL
  const url = `${baseUrl}/home/new`
  const session_cookie = await getCookies()
  const res = await fetch(url, {
    headers: {
      Cookie: `${session_cookie?.name}=${session_cookie?.value}`
    }
  })
  const result = await res.json()
  return result
}

export async function testProducer(): Promise<any> {
  const baseUrl = process.env.BACKEND_INTERNAL_URL || process.env.NEXT_PUBLIC_API_URL
  const url = `${baseUrl}/home/test`

  const session_cookie = await getCookies()
  const res = await fetch(url, {
    headers: {
      Cookie: `${session_cookie?.name}=${session_cookie?.value}`
    }
  })
  const result = await res.json()
  return result
}

