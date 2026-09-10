"use client";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { login, register } from "@/services/authApi";
import { setAccessToken } from "@/services/identity";
export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false); const [error, setError] = useState(""); const router = useRouter();
  async function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); setError(""); const data = new FormData(event.currentTarget); try { const response = isRegister ? await register(String(data.get("email")), String(data.get("password")), String(data.get("name"))) : await login(String(data.get("email")), String(data.get("password"))); setAccessToken(response.access_token); router.push("/"); router.refresh(); } catch (err) { setError(err instanceof Error ? err.message : "操作失败"); } }
  return <section className="auth-panel"><h1>{isRegister ? "创建账户" : "登录"}</h1><form onSubmit={submit}>{isRegister && <label>昵称<input required name="name" maxLength={100} /></label>}<label>邮箱<input required name="email" type="email" /></label><label>密码<input required name="password" type="password" minLength={8} /></label>{error && <p role="alert">{error}</p>}<button type="submit">{isRegister ? "注册并登录" : "登录"}</button></form><button onClick={() => setIsRegister(!isRegister)}>{isRegister ? "已有账户？去登录" : "没有账户？注册"}</button></section>;
}
