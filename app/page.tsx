"use client"

import { useState } from "react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Video, Mic, MessageSquare, Share, Upload, MoreVertical, Settings, Download, Users } from "lucide-react"

export default function VideoConference() {
  const [activeTab, setActiveTab] = useState("screen")
  const [isSharingScreen, setIsSharingScreen] = useState(false)

  const handleShareScreen = () => {
    setIsSharingScreen(true)
  }

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-purple-900 to-purple-700">
      {/* Header */}
      <header className="p-4 flex items-center justify-between">
        <div className="flex flex-col text-white">
          <h1 className="text-xl font-bold">AI Strategy Meeting</h1>
          <p className="text-sm opacity-80">Duration: 45:23</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" className="text-white">
            <Users className="h-4 w-4 mr-2" />4 Participants
          </Button>
          <Button variant="ghost" size="sm" className="text-white">
            Manage Participants
          </Button>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon" className="rounded-full bg-white/10 text-white">
            <Download className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon" className="rounded-full bg-white/10 text-white">
            <Settings className="h-5 w-5" />
          </Button>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 p-4 flex flex-col">
        <div className="flex-1 grid grid-cols-4 gap-4 relative">
          {/* Participants */}
          <Card className="col-span-1 bg-purple-800/50 border-purple-600 text-white">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <Avatar className="h-12 w-12 border-2 border-green-500">
                  <AvatarImage src="/diverse-group-city.png" alt="Analytics AI" />
                  <AvatarFallback>AI</AvatarFallback>
                </Avatar>
                <div>
                  <h3 className="font-medium">Analytics AI</h3>
                  <p className="text-xs opacity-80">Data Analyst</p>
                  <div className="text-xs mt-1 bg-purple-700 rounded px-2 py-0.5 inline-block">Grade 3</div>
                </div>
                <Button variant="ghost" size="icon" className="ml-auto">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </div>
              <div className="mt-2 text-xs opacity-70">Claude AI</div>
            </CardContent>
          </Card>

          {/* Main screen */}
          <Card className="col-span-2 row-span-2 bg-purple-800/30 border-purple-600 flex items-center justify-center relative">
            <CardContent className="p-0 w-full h-full flex items-center justify-center">
              {isSharingScreen ? (
                <div className="w-full h-full p-6">
                  <div className="bg-white rounded-lg w-full h-full flex items-center justify-center">
                    <p className="text-gray-500">Screen content being shared</p>
                  </div>
                </div>
              ) : (
                <div className="text-center p-8 max-w-md">
                  <div className="bg-white/10 backdrop-blur-sm rounded-full p-8 mb-6 inline-flex">
                    <Share className="h-12 w-12 text-white" />
                  </div>
                  <h2 className="text-xl font-medium text-white mb-2">Click to Share Screen or Document</h2>
                  <p className="text-sm text-white/70 mb-6">
                    You'll need to grant permission in your browser when prompted. Make sure to select the window or
                    screen you want to share.
                  </p>

                  <Tabs defaultValue="screen" className="w-full">
                    <TabsList className="grid grid-cols-3 bg-purple-700/50">
                      <TabsTrigger value="screen">Screen Share</TabsTrigger>
                      <TabsTrigger value="document">Document</TabsTrigger>
                      <TabsTrigger value="canvas">Canvas</TabsTrigger>
                    </TabsList>
                  </Tabs>

                  <div className="flex gap-4 mt-6 justify-center">
                    <Button onClick={handleShareScreen} className="bg-purple-600 hover:bg-purple-700">
                      <Share className="h-4 w-4 mr-2" />
                      Share Screen
                    </Button>
                    <Button variant="outline" className="text-white border-white/30 hover:bg-white/10">
                      <Upload className="h-4 w-4 mr-2" />
                      Upload Document
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>

            {/* Active speaker info */}
            <div className="absolute top-4 left-0 right-0 flex justify-center">
              <div className="bg-purple-900/70 backdrop-blur-sm rounded-lg px-4 py-2 flex items-center gap-3">
                <Avatar className="h-10 w-10 border-2 border-green-500">
                  <AvatarImage src="/contemplative-artist.png" alt="Sarah Johnson" />
                  <AvatarFallback>SJ</AvatarFallback>
                </Avatar>
                <div className="text-white">
                  <h3 className="font-medium">Sarah Johnson</h3>
                  <div className="flex items-center gap-4 text-xs">
                    <span>Project Manager</span>
                    <span className="flex items-center gap-1">
                      <span className="h-1.5 w-1.5 rounded-full bg-green-500 inline-block"></span>
                      Acme Corp
                    </span>
                  </div>
                </div>
                <Button variant="ghost" size="icon" className="ml-4 text-white">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </Card>

          <Card className="col-span-1 bg-purple-800/50 border-purple-600 text-white">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <Avatar className="h-12 w-12 border-2 border-green-500">
                  <AvatarImage src="/futuristic-helper-bot.png" alt="AI Assistant" />
                  <AvatarFallback>AI</AvatarFallback>
                </Avatar>
                <div>
                  <h3 className="font-medium">AI Assistant</h3>
                  <p className="text-xs opacity-80">Meeting Facilitator</p>
                  <div className="text-xs mt-1 bg-purple-700 rounded px-2 py-0.5 inline-block">GPT-4</div>
                </div>
                <Button variant="ghost" size="icon" className="ml-auto">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </div>
              <div className="mt-2 text-xs opacity-70">OpenAI</div>
            </CardContent>
          </Card>

          <Card className="col-span-1 bg-purple-800/50 border-purple-600 text-white">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <Avatar className="h-12 w-12 border-2 border-green-500">
                  <AvatarImage src="/contemplative-man.png" alt="John Smith" />
                  <AvatarFallback>JS</AvatarFallback>
                </Avatar>
                <div>
                  <h3 className="font-medium">John Smith</h3>
                  <p className="text-xs opacity-80">Developer</p>
                </div>
                <Button variant="ghost" size="icon" className="ml-auto">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </div>
              <div className="mt-2 flex items-center gap-4 text-xs opacity-70">
                <span className="flex items-center gap-1">
                  <span className="h-1.5 w-1.5 rounded-full bg-green-500 inline-block"></span>
                  Tech Inc
                </span>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Footer controls */}
      <footer className="p-4 flex justify-center">
        <div className="flex gap-4">
          <Button variant="outline" className="bg-purple-800/50 border-purple-600 text-white hover:bg-purple-700 px-6">
            <Video className="h-5 w-5 mr-2" />
            Video
          </Button>
          <Button variant="outline" className="bg-purple-800/50 border-purple-600 text-white hover:bg-purple-700 px-6">
            <Mic className="h-5 w-5 mr-2" />
            Audio
          </Button>
          <Button variant="outline" className="bg-purple-800/50 border-purple-600 text-white hover:bg-purple-700 px-6">
            <MessageSquare className="h-5 w-5 mr-2" />
            Chat
          </Button>
        </div>
      </footer>
    </div>
  )
}
