import discord
import requests
import asyncio
import collections
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from discord.ext import commands
import json
import random

class QandA(commands.Cog):
    scores = collections.defaultdict(int)
    questions = collections.defaultdict(str)

    def __init__(self, client):
        self.client = client
        j = ''
        with open('200k_questions.json', 'r') as f:
            j = f.read()
        self.questions = json.loads(j)

    def HTMLtoMarkdown(self, s):
        s = s.replace('<i>', '*')
        s = s.replace('</i>', '*')
        s = s.replace('<b>', '**')
        s = s.replace('</b>', '**')
        s = s.replace('<br />', '\n')
        return s

    @commands.slash_command(brief="Get a question." ,description="Get a question. Answer within 30 seconds.")
    async def q(self, ctx):
        #get random question
        content = self.questions[random.randint(0, len(self.questions)-1)]
        print(content)
            
        category = content["category"]
        value = int(content["value"].replace('$', '').replace(',', ''))
        question = self.HTMLtoMarkdown(content["question"])
        answer = self.HTMLtoMarkdown(content["answer"])

        embed=discord.Embed(title=f'{category} for ${value}', description=question, color=0x004cff)
        #embed.add_field(name="Question", value=question, inline=False)

        print(f'Category:{category} for ${value}\nQuestion: {question}\nAnswer: {answer}')
        await ctx.respond(embed=embed)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel 
            

        try:
            msg = await self.client.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            timeout = discord.Embed(title="Time's up!", description=f"We were looking for \"{answer}\"", color=0xff0000)
            await  ctx.respond(embed=timeout)
            #await ctx.send(f"Sorry! Time's up!\nThe answer was \"{answer}\"")
        else:
            diff = fuzz.WRatio(msg.content, answer)
            print(f'{msg.content} = {answer}\n {diff}% match')
            if diff > 70:
                correct = discord.Embed(title="Correct!", description=f"You got it! The answer was \"{answer}\"", color=0x00ff00)
                await ctx.respond(embed=correct)
                #await ctx.send('Correct!')
                self.scores[msg.author] += value
            else:
                incorrect = discord.Embed(title="Incorrect!", description=f"We were looking for \"{answer}\"", color=0xff0000)
                await ctx.respond(embed=incorrect)
                #await ctx.send(f"Incorrect.\nThe answer was {answer}")

    @commands.slash_command(description="See your score.")
    async def score(self, ctx):
        print(self.scores)
        #create scoreboard embed
        embed=discord.Embed(title="Scoreboard", color=0x004cff)
        if ctx.author in self.scores:
            embed.add_field(name=ctx.author.name, value=self.scores[ctx.author], inline=False)
        else:
            embed.add_field(name=ctx.author.name, value=0, inline=False)

        await ctx.respond(embed=embed)

def setup(client):
    client.add_cog(QandA(client))