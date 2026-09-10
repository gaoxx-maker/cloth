import Link from "next/link";
import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <nav>
          <Link href="/">Fashion Explorer</Link>
          <Link href="/login">登录</Link>
          <Link href="/account">我的喜欢</Link>
          <Link href="/experiment">实验数据</Link>
        </nav>
        <main>{children}</main>
      </body>
    </html>
  );
}
